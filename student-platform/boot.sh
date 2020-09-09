#!/bin/sh

source venv/bin/activate
while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo "Upgrage command failed, retrying in 5 sec..."
    sleep 5
done
exec gunicorn -b :5000 --access-logfile - --error-logfile - student_platform:app