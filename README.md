# Log Your Incidents

## How to Run the Application Locally
The code can be accessed through from the website GitHub:
https://github.com/AmyHdigital/LogYourIncident

It is assumed that Python 3.9+ is installed on the target machine.
1. Create the virtual environment – in this case I have called it env:

`python3 -m venv env` 

2. Activate the virtual environment:

`source env/bin/activate`

3. Install the dependencies in the requirements.txt:

`python3 -m pip install -r requirements.txt`

4. Export the secret key:

`export SECRET_KEY=abcdefg (can be anything!) `

5. Create the database tables: 

`python manage.py migrate `

6. Create the super user with email and password:

`python manage.py createsuperuser` 

7. Populate the base data:

`python manage.py loaddata system.json`

8. Run the server:

`python manage.py runserver`














