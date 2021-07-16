# Capstone Project - Casting Agency

The URL the application is hosted in is: 
https://ifat--casting-agency-heroku.herokuapp.com/ | https://git.heroku.com/ifat--casting-agency-heroku.git


### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/flaskr` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the root directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Endpoints

GET '/actors'
- Fetches a set of actors

GET '/movies/'
- Fetches a set of movies

DELETE '/actors/${id}'
- Deletes a specified actor using the id of the actor
- Request Arguments: id - integer
- Returns: The id of the actor deleted

POST '/actors'
- Sends a post request in order to add an actor
- Request Body: 
{'name': '',
'age': '',
'gender': ''}
- Returns: all of the actors in the API

PATCH '/actors/${id}'
- Sends a patch request in order to edit a specific actor details
- Request Body: 
{'name': '',
'age': '',
'gender': ''}
- Returns: all of the actors in the API

DELETE '/movies/${id}'
- Deletes a specified movie using the id of the movie
- Request Arguments: id - integer
- Returns: The id of the movie deleted


POST '/movies'
- Sends a post request in order to add a movie
- Request Body: 
{'title': '',
'release_date': ''}
- Returns: all of the movies in the API

PATCH '/movies/${id}'
- Sends a patch request in order to edit a specific movie details
- Request Body: 
{'title': '',
'release_date': ''}
- Returns: all of the movies in the API


## Permissions

Casting Assistant:
get:actors
get:movies

Casting Director:
delete:actors
get:actors
get:movies
patch:actors
patch:movies
post:actor

Executive Producer:
delete:actors
delete:movies
get:actors
get:movies
patch:actors
patch:movies
post:actors
post:movies


## Testing Instructions

To run the tests, run
```
dropdb casting_agency_test
createdb casting_agency_test
psql casting_agency_test < casting_agency_test.psql
python test_flaskr.py
```

### Authentication Setup

- Go to:
fsnd-ifat.eu.auth0.com/authorize?audience=casting_agency&response_type=token&client_id=2VS6WrOUWVY0lguOqpsPQKFdrkNwnPw2&redirect_uri=https://127.0.0.1:5000/login-results

- Sign into each account and make note of the JWT, with the following credentials:
	user: castingassistant@udacity.com, password: castingassistant!@#123456
	user: castingdirector@udacity.com, password: castingdirector!@#123456
	user: executiveproducer@udacity.com, password: executiveproducer!@#123456

- Update the tokens you get for each user in the setup.sh file in the base dir.
- Export in the terminal inside the virtuel enviroment, all of the tokens. (example: export EXECUTIVE_PRODUCER_TOKEN="eyJhbGci....")
