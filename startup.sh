python manage.py migrate
python manage.py createsuperuser   --no-input
python manage.py loaddata system.json
gunicorn incidentApp.wsgi