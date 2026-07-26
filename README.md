# Workout Application (Backend)
- RESTful API built with Flask, SQLAlchemy, and Marshmallow.
- It allows users to create and manage workouts, exercises, and the relationship between them through a join table.
- This application demonstrates database relationships, model validations, schema validations, serialization, and CRUD operations using Flask.

## Features
* Create, view, and delete workouts and exercises
* Add an exercise to a workout
* Many-to-many relationship between workouts and exercises
* Model validations
* Schema validations using Marshmallow
* Database constraints
* Seed file for generating sample data

## Built using:
- Python3
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- Marshmallow
- SQLite
- Pipenv

## Installation
- Clone the repository: https://github.com/daisy-koech/flask-sqlalchemy
- Navigate into the project
- Install dependencies
- Activate the virtual environment

## Database Setup
- Initialize and apply the database migrations
- If migrations have not yet been created:
    flask db init
    flask db migrate -m "Initial migration"
    flask db upgrade

## Running the Application
- Start the Flask server:
-The application will run on:
    http://127.0.0.1:5555

# Database Models
## Exercise
- id
- name
- category
*-equipment_needed

## Workout
- id
- duration_minutes
- notes

## WorkoutExercise
- workout_id
- exercise_id
- reps
- sets
- duration_seconds
