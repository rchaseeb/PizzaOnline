#!/bin/bash
#while true
#do
        echo "i am running now"
        #sleep 2
#done
python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py dump_data

python manage.py runserver 0.0.0.0:8000
