# Log Your Incidents

## Usage
This project is designed to be deployed to Heroku with a
PostgreSQL database.  However, it also contains a local
settings file that allows it to work with a SQLLite 
database.

To create the database tables (for PostgreSQL):

```
python manage.py migrate
```

For local running (SQLLite):
```
python manage.py migrate --settings=incidentApp.local_settings 
```

You then need to create the admin (superuser):
```
python manage.py createsuperuser
```

Or, if running locally using SQLLite:
```
python manage.py createsuperuser --settings=incidentApp.local_settings 
```

Once the database tables have been created, start the
server with (for PostgreSQL:

```
python manage.py runserver
```

or (for SQLLite)

```
python manage.py runserver --settings=incidentApp.local_settings   
```

Admin pages can be access via the special URL:

https://(hostname)/admin

and then logging in as the admin/superuser