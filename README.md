[![Build Status](https://travis-ci.org/andela-egichuri/checkpoint3.svg?branch=master)](https://travis-ci.org/andela-egichuri/checkpoint3) [![Coverage Status](https://coveralls.io/repos/github/andela-egichuri/checkpoint3/badge.svg?branch=develop)](https://coveralls.io/github/andela-egichuri/checkpoint3?branch=develop) [![Code Issues](https://www.quantifiedcode.com/api/v1/project/f3c29d30fe484ec4b735155f3d53e4e6/snapshot/origin:develop:HEAD/badge.svg)](https://www.quantifiedcode.com/app/project/f3c29d30fe484ec4b735155f3d53e4e6)

# Checkpoint 3
Application - Django Powered BucketList Application

## Usage Instructions:
Before installation ensure the following are installed in your system:
 - Python
 - A relational database (Postgres has been used for development and testing).

*All other dependencies are in `requirements.txt`*

* Download or clone the repo
* Install requirements.
`pip install -r requirements.txt`
* Setup environment variables
```
DATABASE_URL="postgres://<user>:<password>@localhost:5432/<db_name>"
SECRET=<SECRET>
```
* Perform database migrations.
```
python manage.py makemigrations
python manage.py migrate
```
* Run the application
`python manage.py runserver`

## EndPoints
Access to all endpoints except user login and registration requires authentication.

The API endpoints are documented [here](http://mybl-app.herokuapp.com/api/docs/)

## Features
You can try out the app [here](http://mybl-app.herokuapp.com/)

## Testing
Tests are run from the root folder
`python manage.py test`

To show Coverage results
`coverage report -m`
