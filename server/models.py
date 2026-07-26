from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint
from sqlalchemy.orm import validates, relationship

db = SQLAlchemy()

class Exercise(db.Model):
    __tablename__ = "exercises"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = relationship("WorkoutExercise",
                                     back_populates="exercise", cascade="all, delete-orphan")

    workouts = relationship("Workout",
                             secondary="workout_exercises", back_populates="exercises")

    @validates("name")
    def validate_name(self, key, name):
        if not name or name.strip():
            raise ValueError(
                "Exercise name cannot be empty"
            )
        return name

    @validates("category")
    def validate_category(self, key, category):
        allowed_categories = [
            "Strength",
            "Cardio",
            "Flexibility",
            "Core"
        ]
        if category not in allowed_categories:
            raise ValueError(
                "Invalid exercise category"
            )
        return category

class Workout(db.Model):
    __tablename__ = "workouts"

    __table_args__ = (
        CheckConstraint(
            "duration_minutes > 0",
            name="positive_duration"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes =  db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)

    workout_exercises = relationship("WorkoutExercise",
                                     back_populates="workout", cascade="all, delete-orphan")

    exercises = relationship("Exercise", 
                             secondary="workout_exercises",
                             back_populates="workouts")

    @validates("duration_minutes")
    def validate_duration(self, key, duration):
        if duration <= 0:
            raise ValueError("Workout duration must be greater than zero")
        return duration

class WorkoutExercise(db.Model):
    __tablename__ = "workout_exercises"

    __table_args__ = (CheckConstraint(
            "reps >= 0",
            name="positive_reps"
        ),
        CheckConstraint(
            "sets >= 0",
            name="positive_sets"
        ),
        CheckConstraint(
            "duration_seconds >= 0",
            name="positive_seconds"
        )
    )

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey("workouts.id"), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey("exercises.id"), nullable=False)

    reps = db.Column(db.Integer)
    sets = db.Column(db.Integer)
    duration_seconds = db.Column(db.Integer)

    workout = relationship("Workout",
                           back_populates="workout_exercises")
                           
    exercise = relationship("Exercise",
                            back_populates="workout_exercises")

    @validates("reps", "sets", "duration_seconds")
    def validate_positive_numbers(self, key, value):
        if value is not None and value < 0:
            raise ValueError(
                f"{key} cannot be negative"
            )
        return value
