#!/bin/sh

until cd /app
do
    echo "Waiting for server volume..."
done

current_version=$(alembic current)
heads_version=$(alembic heads)

if [ "$current_version" == "$heads_version" ]; then
    echo "Current version ($current_version) is up to date with heads version ($heads_version)."
else
    echo "Current version ($current_version) is NOT up to date with heads version ($heads_version)."

    alembic revision --autogenerate -m "up to last change"
    alembic upgrade head
fi

python app/main.py