#!/usr/bin/env python3

from datetime import date
from app import app
from models import db, Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Clearing database...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    pushups = Exercise(
        name="Push Ups",
        category="Strength",
        equipment_needed=False
    )
    running = Exercise(
        name="Running",
        category="Cardio",
        equipment_needed=False
    )
    stretching = Exercise(
        name="Stretching",
        category="Flexibility",
        equipment_needed=False
    )
    db.session.add_all([
        pushups,
        running,
        stretching
    ])
    db.session.commit()

    print("Creating workouts...")
    workout1 = Workout(
        date=date(2026, 7, 26),
        duration_minutes=45,
        notes="Morning strength workout"
    )
    workout2 = Workout(
        date=date(2026, 7, 27),
        duration_minutes=30,
        notes="Cardio session"
    )
    db.session.add_all([
        workout1,
        workout2
    ])
    db.session.commit()

    print("Adding exercises to workouts...")
    workout_exercise1 = WorkoutExercise(
        workout_id=workout1.id,
        exercise_id=pushups.id,
        reps=15,
        sets=3
    )
    workout_exercise2 = WorkoutExercise(
        workout_id=workout2.id,
        exercise_id=running.id,
        duration_seconds=1800
    )
    db.session.add_all([
        workout_exercise1,
        workout_exercise2
    ])
    db.session.commit()

    print("Database seeded successfully!")
