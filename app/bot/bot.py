import re
from asyncio import gather

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from pyrogram.types import Message
from pyrogram_patch import patch
from pyrogram_patch.fsm import State
from pyrogram_patch.fsm.filter import StateFilter
from pyrogram_patch.fsm.storages import MemoryStorage
from pyrogram_patch.router import Router

from bot_utils import get_inline_keyboard
from config.dbsettings import bot_settings
from database.repositories import alchemy_repository as repository
from database.schemas.user_schema import UserCreate
from database.schemas.user_task_schema import UserTaskCreate, UserTaskUpdatePartial
from fsm.state_groups.login_group import LoginGroup
from fsm.state_groups.navigation_group import NavigationGroup
from fsm.state_groups.task_change import TaskChangeGroup
from fsm.state_groups.task_creating import TaskGroup
from keyboard.main_keyboard import main_keyboard

app = Client(bot_settings.BOT_NAME,
             api_id=bot_settings.API_ID,
             api_hash=bot_settings.API_HASH,
             bot_token=bot_settings.BOT_TOKEN)

login_router = Router()

tasks = Router()
patched_app = patch(app)
patched_app.set_storage(MemoryStorage())
patched_app.include_router(login_router)
patched_app.include_router(tasks)


@app.on_message(filters.command("start"))
async def start_cmd(client: Client, message: Message, state: State) -> None:
    """
    Обработка команды /start
    
    @param client: 
    @param message: 
    @param state: 
    """
    user = await repository.get_user(message.from_user.id)
    if user:
        await state.set_state(NavigationGroup.main_menu)
        await message.reply("C возвращением", reply_markup=main_keyboard)

        # todo set main keyboard
    else:
        await state.set_state(NavigationGroup.registration)
        await message.reply("Привет! Чтобы зарегистрироваться, введите /register.")


@login_router.on_message(filters.command("register") & StateFilter(NavigationGroup.registration))
async def register_cmd(client: Client, message: Message, state: State) -> None:
    """
    Обработка команды /register
    @param client: 
    @param message: 
    @param state: 
    """
    await message.reply("Введите ваш логин:")
    await state.set_state(LoginGroup.login)


@login_router.on_message(filters=filters.text & StateFilter(LoginGroup.login))
async def enter_login(client: Client, message: Message, state: State) -> None:
    """
    Обработка введенного login
    
    @param client: 
    @param message: 
    @param state: 
    @return: 
    """
    login = await repository.check_unique_login(message.text)
    if login:
        await message.reply("Логин уже используется. Повторите ввод.")
        return None

    await state.set_data({'login': message.text})
    await message.reply("Введите ваше имя:")
    await state.set_state(LoginGroup.name)


@login_router.on_message(filters=filters.text & StateFilter(LoginGroup.name))
async def enter_name(client: Client, message: Message, state: State) -> None:
    """
    Обработка введенного имени.
    
    @param client: 
    @param message: 
    @param state: 
    """
    await state.set_data({'name': message.text})
    data = await state.get_data()
    try:
        await repository.add_user(UserCreate(
            login=data.get('login'),
            user_telegram_id=message.from_user.id,
            password='123123123',  # todo add hash with sold
            name=data.get('name'))
        )
    except Exception as ex:
        await message.reply("произошла ошибка повторите попытку")
    await message.reply("Регистрация успешна",
                        reply_markup=main_keyboard)
    await state.set_state(NavigationGroup.main_menu)


@tasks.on_message(filters.regex("Create task") & StateFilter(NavigationGroup.main_menu))
async def create_task_cmd(client: Client, message: Message, state: State) -> None:
    """
    Обработка команды создания задачи из ReplyKeyboard.

    @param client:
    @param message:
    @param state:
    """
    await message.reply("Введите заголовок задачи:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(TaskGroup.title)


@tasks.on_message(filters.text & StateFilter(TaskGroup.title))
async def create_task_title_cmd(client: Client, message: Message, state: State) -> None:
    """
    Обработка ввода заголовка новой задачи

    @param client:
    @param message:
    @param state:
    """
    await state.set_data({'title': message.text})
    await message.reply("Введите текст задачи:")
    await state.set_state(TaskGroup.message)


@tasks.on_message(filters.text & StateFilter(TaskGroup.message))
async def create_task_message_cmd(client: Client, message: Message, state: State) -> None:
    """
    Обработка ввода тела новой задачи.
    @param client:
    @param message:
    @param state:
    """
    await state.set_data({'message': message.text})
    data = await state.get_data()
    user = await repository.get_user(message.from_user.id)
    await repository.add_task(
        UserTaskCreate(
            title=data.get('title'),
            message=data.get('message'),
            user_id=user.id)
    )
    await message.reply('Задача создана', reply_markup=main_keyboard)
    await state.set_state(NavigationGroup.main_menu)


@tasks.on_message(filters.regex("Show tasks") & StateFilter(NavigationGroup.main_menu))
async def show_all_tasks(client: Client, message: Message, state: State) -> None:
    """
    Обработка команды показа всех задач из ReplyKeyboard.

    @param client:
    @param message:
    @param state:
    """
    user_tasks = await repository.get_user_tasks(message.from_user.id)
    keyboard = get_inline_keyboard(
        user_tasks,
        item_handling=lambda x: (x.id, f'{x.title} {x.is_done}'),
        command='task',
    )

    if keyboard:
        tasks_inline_keyboard = InlineKeyboardMarkup(keyboard)

        await message.reply(
            'Ваши задачи',
            reply_markup=tasks_inline_keyboard
        )
    else:
        await message.reply(
            'Тут пока пусто'
        )


@tasks.on_callback_query(filters.regex("taskoffset,offset"))
async def change_all_tasks_query(client: Client, callback_query: CallbackQuery) -> None:
    """
    Обработка кнопок пагинации задач

    @param client:
    @param callback_query:
    """
    digits = re.search(r'offset:(?P<offset>\d+)', callback_query.data).groupdict()
    offset = int(digits["offset"])
    user_tasks = await repository.get_user_tasks(callback_query.from_user.id, offset=offset)
    keyboard = get_inline_keyboard(user_tasks,
                                   item_handling=lambda x: (x.id, f'{x.title} {x.is_done}'),
                                   command='task',
                                   offset=offset)
    tasks_inline_keyboard = InlineKeyboardMarkup(keyboard)

    await callback_query.edit_message_text(text='Ваши задачи',
                                           reply_markup=tasks_inline_keyboard)


@tasks.on_callback_query(filters.regex("^task,"))
async def show_task_options(client: Client, callback_query: CallbackQuery) -> None:
    """
    Показ опций над задачей
    @param client:
    @param callback_query:
    """
    digits = re.search(r'id:(?P<task_id>\d+)offset:(?P<offset>\d+)', callback_query.data).groupdict()
    task_id, offset = digits['task_id'], digits['offset']
    user_task = await repository.get_task(task_id)
    keyboard = [
        [InlineKeyboardButton(text='Просмотр', callback_data=f'taskshow,id:{task_id}')],
        [InlineKeyboardButton(text='Изменить', callback_data=f'taskchange,id:{task_id}')],
        [InlineKeyboardButton(text='Удалить', callback_data=f'taskdelete,id:{task_id}')],
    ]
    if not user_task.is_done:
        keyboard.append(
            [InlineKeyboardButton(text='Отметить как выполнена', callback_data=f'taskdone,id:{task_id}')]
        )
    keyboard.append([InlineKeyboardButton(text='Назад', callback_data=f'taskoffset,offset:{offset}')])
    tasks_inline_options_keyboard = InlineKeyboardMarkup(keyboard)
    await callback_query.edit_message_text('Опции задачи',
                                           reply_markup=tasks_inline_options_keyboard)


@tasks.on_callback_query(filters.regex("^taskshow,"))
async def show_task(client: Client, callback_query: CallbackQuery) -> None:
    """
    Показ полного текста задачи

    @param client:
    @param callback_query:
    """
    digits = re.search(r'id:(?P<task_id>\d+)', callback_query.data).groupdict()
    task_id = digits['task_id']
    user_task = await repository.get_task(task_id)
    await client.send_message(
        callback_query.from_user.id,
        text=f'title:\n{user_task.title}\nmessage:\n{user_task.message}'
    )


@tasks.on_callback_query(filters.regex("^taskdone,"))
async def task_done(client: Client, callback_query: CallbackQuery, state: State) -> None:
    """
    Отметить задачу как выполненная
    @param client:
    @param callback_query:
    @param state:
    """
    digits = re.search(r'id:(?P<task_id>\d+)', callback_query.data).groupdict()
    task_id = digits['task_id']
    user_task = await repository.get_task(task_id)
    await repository.update_task(
        task_in=user_task,
        user_task_update=UserTaskUpdatePartial(is_done=True),
        partial=True
    )
    await client.delete_messages(callback_query.from_user.id, callback_query.message.id)
    await client.send_message(
        callback_query.from_user.id,
        text=f'Задача отмечена как выполненная'
    )
    await state.set_state(NavigationGroup.main_menu)


@tasks.on_callback_query(filters.regex("^taskdelete,"))
async def task_delete(client: Client, callback_query: CallbackQuery, state: State) -> None:
    """
    Удалить задачу
    @param client:
    @param callback_query:
    @param state:
    """
    digits = re.search(r'id:(?P<task_id>\d+)', callback_query.data).groupdict()
    task_id = digits['task_id']
    user_task = await repository.get_task(task_id)
    await repository.delete_task(user_task)

    await client.delete_messages(callback_query.from_user.id, callback_query.message.id)
    await client.send_message(
        callback_query.from_user.id,
        text=f'Задача удалена'
    )


@tasks.on_callback_query(filters.regex("^taskchange,"))
async def change_task(client: Client, callback_query: CallbackQuery, state: State) -> None:
    """
    Изменить задачу

    @param client:
    @param callback_query:
    @param state:
    """
    digits = re.search(r'id:(?P<task_id>\d+)', callback_query.data).groupdict()
    task_id = digits['task_id']
    user_task = await repository.get_task(task_id)

    await gather(
        client.delete_messages(callback_query.from_user.id, callback_query.message.id),
        client.send_message(
            callback_query.from_user.id,
            text=f'title:\n{user_task.title}\nmessage:\n{user_task.message}'
        ),
        client.send_message(
            callback_query.from_user.id,
            text=f'Замените заголовок или введите /empty',
            reply_markup=ReplyKeyboardRemove()
        ),
        callback_query.edit_message_reply_markup(reply_markup=None),
        state.set_state(TaskChangeGroup.title),
        state.set_data({'user_task': user_task})
    )


@tasks.on_message(StateFilter(TaskChangeGroup.title))
async def change_task_title(client: Client, message: Message, state: State) -> None:
    """
    Изменить заголовок задачи
    @param client:
    @param message:
    @param state:
    """
    message_text = message.text
    if message_text != '/empty':
        await state.set_data({'title': message_text})

    await message.reply(f'Замените текст задачи или введите /empty')
    await state.set_state(TaskChangeGroup.message)


@tasks.on_message(StateFilter(TaskChangeGroup.message))
async def change_task_message(client: Client, message: Message, state: State) -> None:
    """
    Изменить текст задачи

    @param client:
    @param message:
    @param state:
    """
    message_text = message.text
    if message_text != '/empty':
        await state.set_data({'message': message_text})

    data = await state.get_data()
    task_update = UserTaskUpdatePartial(**{key: value for key, value in data.items() if key not in ('user_task',)})

    await repository.update_task(
        task_in=data['user_task'],
        user_task_update=task_update,
        partial=True
    )
    await state.set_state(NavigationGroup.main_menu)
    await message.reply('Задача изменена',
                        reply_markup=main_keyboard)


app.run()
