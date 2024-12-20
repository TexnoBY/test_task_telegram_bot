***Тестовое задание: Разработка бота с использованием Pyrogram и FSM***
-----------------------
[Обзор проекта](https://github.com/TexnoBY/test_task_telegram_bot/blob/master/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%20%D1%80%D0%B0%D0%B1%D0%BE%D1%82%D1%8B.mp4)
# Зависимссти
- python 3.12
- requirements.txt 
Пример
# Установка
Перед запуском вам необходимо получить токен для вашего будущего бота у бота Telegram @BotFather, 
а так же API_ID и API_HASH по ссылке https://my.telegram.org
<br/>
Импортировать репозиторий удобным вам способом.
<br/>
После этого выберите удобный для вас способ запуска ниже.
## Обычный
 - Необходимо установить Python 3.12 https://www.python.org/downloads/release/python-3128/
 - Установить все зависимости коммандой `pip install -r requirements.txt`
 - Заменить получение ранее BOT_TOKEN, API_ID, API_HASH в файле [конфигурации бота](https://github.com/TexnoBY/test_task_telegram_bot/blob/master/app/bot/bot_config.py)

 - Получить и применить миграции
 <br/>
 `alembic revision --autogenerate -m "Comment"` 
 <br/>
 `alembic upgrade head`
 - Запустить бота
  `python app/main.py`
## Docker
  - Установить Docker
  - Заменить получение ранее BOT_TOKEN, API_ID, API_HASH в файле [docker-compose.yml](https://github.com/TexnoBY/test_task_telegram_bot/blob/master/docker-compose.yml)
  - Запуск скрипка `docker compose -f docker-compose.yml -p Name up -d`

# Описание
- База данных представлена 2 таблицами 

![Схема БД](DBScheme.svg)
 <br/>
 <br/>
- Схема работы бота
- ![Схема бота](BotFSM.svg)

- Для управления состояниями использовался [репозиторий](https://github.com/kotttee/pyrogram_patch)
 предоставляющий управлениями состояниями схожее с библиотекой [aiogram](https://github.com/aiogram/aiogram)
### Модуль database

Модуль database писался как автономный и расширяемый, что значит добавив новый [db_helper](https://github.com/TexnoBY/test_task_telegram_bot/tree/master/app/database/db_helpers) и [repository](https://github.com/TexnoBY/test_task_telegram_bot/tree/master/app/database/repositories) для управления данными, например, MongoDB или любой другой удобный метод и моделей, соответсвующих [схемам](https://github.com/TexnoBY/test_task_telegram_bot/tree/master/app/database/schemas), и реализовав методы из [класса](https://github.com/TexnoBY/test_task_telegram_bot/blob/master/app/database/repositories/base_crud_repository.py) можно легко поменять метод хранения. Это не потребует переписывания самого бота
