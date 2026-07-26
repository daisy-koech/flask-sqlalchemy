from schemas import (workout_schema, workouts_schema, exercise_schema, exercises_schema, workout_exercise_schema, workout_exercises_schema)
from flask import Flask, make_response, request
from flask_migrate import Migrate
from models import db, Workout, Exercise, WorkoutExercise

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

migrate = Migrate(app, db)

#----------------Endpoints-------------------------
# GET (workouts)
@app.route("/workouts", methods=["GET"])
def get_workouts():
    workouts = Workout.query.all()
    return make_response(workouts_schema.dump(workouts), 200)

#GET one workout
@app.route("/workouts/<int:id>", methods=["GET"])
def get_workout(id):
    workout = Workout.query.get(id)

    if not workout:
        return {"error": "Workout not found"}, 404
    return make_response(workout_schema.dump(workout),200)

#POST
@app.route("/workouts", methods=["POST"])
def create_workout():
    data = request.get_json()

    errors = workout_schema.validate(data)
    if errors:
        return make_response(errors, 400)

    workout = Workout(
        date=data["date"],
        duration_minutes=data["duration_minutes"],
        notes=data.get("notes")
    )
    db.session.add(workout)
    db.session.commit()

    return make_response(workout_schema.dump(workout), 201)

#DELETE
@app.route("/workouts/<id>", methods=["DELETE"])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404

    db.session.delete(workout)
    db.session.commit()
    return {}, 204

#join table
@app.route("/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises", methods=["POST"])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.filter_by(id=workout_id).first()
    exercise = Exercise.query.filter_by(id=exercise_id).first()

    if not workout or not exercise:
        return make_response({"error": "Workout or exercise not found"}, 404)
    
    data = request.get_json()
    workout_exercise = WorkoutExercise(
        workout_id=workout.id,
        exercise_id=exercise.id,
        reps=data.get("reps"),
        sets=data.get("sets"),
        duration_seconds=data.get("duration_seconds")
    )

    db.session.add(workout_exercise)
    db.session.commit()
    return make_response({"message": "Exercise added to workout"}, 201)

#GET (exercises)
@app.route("/exercises", methods=["GET"])
def get_exercises():
    exercises = Exercise.query.all()
    return make_response(
        exercises_schema.dump(exercises),
        200
    )

#GET one exerciose
@app.route("/exercises/<id>", methods=["GET"])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    
    workouts = []
    for workout in exercise.workouts:
        workouts.append({
            "id": workout.id,
            "date": str(workout.date),
            "duration_minutes": workout.duration_minutes
        })
    return make_response(exercise_schema.dump(exercise), 200)

#CREATE exercise
@app.route("/exercises", methods=["POST"])
def create_exercise():
    data = request.get_json()

    errors = exercise_schema.validate(data)
    if errors:
        return make_response(errors, 400)

    exercise = Exercise(
        name=data["name"],
        category=data["category"],
        equipment_needed=data["equipment_needed"]
    )
    db.session.add(exercise)
    db.session.commit()
    return make_response(exercise_schema.dump(exercise), 201)

#DELETE exercise
@app.route("/exercises/<id>", methods=["DELETE"])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404

    db.session.delete(exercise)
    db.session.commit()
    return {}, 204

if __name__ == "__main__":
    app.run(port=5555, debug=True)
