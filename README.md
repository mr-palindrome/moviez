# Moviez

## Description
This is a simple backend web application that allows users to view movies and their details and create their own collection.

## Features
- Users can view a list of movies and their respective genres.
- Users can create their own collection of movies.
- Users can view their collection of movies.
- Users can update the details of their collection.
- Users can delete movies from their collection.
- Users can view the number of requests made to the API.
- Users can reset the number of requests made to the API.

## API Endpoints
- Authentication
    - `POST /register/` - Register a new user
    - `POST /login/` - Login a user
- Movies
    - `GET /movies/` - Get all movies
- Collections
    - `GET /collections/` - Get all collections
    - `POST /collections/` - Create a new collection
    - `GET /collections/:uuid/` - Get a collection
    - `PUT /collections/:uuid/` - Update a collection
    - `DELETE /collections/:uuid/` - Delete a collection
- Management
    - `GET /request-count/` - Get the number of requests made to the API
    - `POST /request-count/rest/` - Reset the number of requests made to the API

## Setup
1. Clone the repository.

    ```bash
    git clone https://github.com/mr-palindrome/moviez.git
    ```
2. Change into the project directory.

    ```bash
    cd moviez
    ```
3. Create a virtual environment.

    ```bash
    python3 -m venv venv
    ```
4. Activate the virtual environment.

    ```bash
    source venv/bin/activate
    ```
5. Install the project dependencies.

    ```bash
    pip install -r requirements.txt
    ```
6. Create a `.env` file in the root of the project and add the following environment variables:

    ```
    SECRET_KEY = 'secret_key'
    MOVIE_API_URL = 'https://demo.credy.in/api/v1/maya/movies/'
    ```
7. Run the migrations.

    ```bash
    python manage.py migrate

8. Run the development server.

    ```bash
    python manage.py runserver
    ```
