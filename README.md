# Capstone Project

## Getting Started

### Installing Dependencies

#### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the root directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.


## Running the server

From within the root directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
export FLASK_APP=api.py
export FLASK_ENV=development
flask run
```

## Api documentation

```
• Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration. 
• Authentication: This application requires authentication from `https://dev-w0twvam7.eu.auth0.com/authorize?audience=capstone&response_type=token&client_id=fIqAzFVMCGHU5zgV3OJBHVowsvY4QQXM&redirect_uri=https://127.0.0.1:5000/movies`
 
Error Handling
Errors are returned as JSON objects in the following format:

{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
The API will return three error types when requests fail:
	• 404: Not Found
	• 422: Unprocessable
    • 405: method not allowed



Endpoints
GET '/actors'
GET '/movies'
DELETE '/actors/<int:actor_id>'
DELETE '/movies/<int:movies_id>'
POST '/actors'
POST '/movies'
PATCH '/actors/<int:actor_id>'
PATCH '/movies/<int:movie_id>'

GET '/actors'
- Fetches a list of actors 
- Request Arguments: Access_Token with role (Casting Assistant) or higher
- Returns: list of actors in groups of 10.
{
    "actors": [
        {
            "age": 25,
            "gender": "male",
            "id": 1,
            "name": "test"
        },
        {
            "age": 25,
            "gender": "male",
            "id": 2,
            "name": "test"
        }
    ],
    "success": true
}

GET '/movies'
- Fetches a list of movies
- Request Arguments: Access_Token with role (Casting Assistant) or higher
- Returns: list of movies in groups of 10.
{
    "movies": [
        {
            "id": 2,
            "release_date": "Sat, 10 Oct 2020 00:00:00 GMT",
            "title": "test"
        },

        {
            "id": 11,
            "release_date": "Sat, 10 Oct 2020 00:00:00 GMT",
            "title": "test"
        }
    ],
    "success": true
}

DELETE '/actors/<int:actor_id>'
- Deletes the actor with the provided id 
- Request Arguments: actor's id and an Access_Token with role (Casting Director) or higher
- Returns: Boolean 'success' true if the actor is deleted or false if there is an error, and the deleted actor id
{
    "actor_id": 2,
    "success": true
}

DELETE '/movies/<int:movie_id>'
- Deletes the movie with the provided id 
- Request Arguments: movie's id and an Access_Token with role (Executive Producer) or higher
- Returns: Boolean 'success' true if the movie is deleted or false if there is an error, and the deleted movie id

{
    "movie_id": 2,
    "success": true
}

POST '/actors'
- Creates new actor.
- Request Arguments: actor's name, actor's age and actor's gender and an Access_Token with role (Casting Director) or higher
- Returns: The created actor details
{
    "actor": {
        "age": 25,
        "gender": "male",
        "id": 19,
        "name": "test"
    },
    "success": true
}

GET '/movies/<int:movie_id>'
- Creates new movie.
- Request Arguments: movie's title, movie's release_date (yyyy-mm-dd) and an Access_Token with role (Executive Producer) or higher
- Returns: The created movie details

{
    "movie": {
        "id": 20,
        "release_date": "Sat, 10 Oct 2020 00:00:00 GMT",
        "title": "test"
    },
    "success": true
}

PATCH '/actors/<int:actor_id>'
- modifies an actor details. 
- Request Arguments: movie's id, movie's title and movie's release_date (yyyy-mm-dd) and an Access_Token with role (Casting Director) or higher
- Returns: The movie details after modification.

{
    "actor": {
        "age": 26,
        "gender": "male",
        "id": 1,
        "name": "modified"
    },
    "success": true
}

PATCH '/movies/<int:movie_id>'
- modifies a movie details. 
- Request Arguments: tmovie's id, movie's title and movie's release_date (yyyy-mm-dd) and an Access_Token with role (Casting Director) or higher
- Returns: The actor details after modification.

{
    "movie": {
        "id": 3,
        "release_date": "Sat, 10 Oct 2020 00:00:00 GMT",
        "title": "modified"
    },
    "success": true
}
```


## Testing
To run the tests, run
```
dropdb capstone_test
createdb capstone_test
python test_app.py
```