# tests/test_database.py

import pytest
from pathlib import Path
from src.database import DatabaseHandler
from src.habit import Habit, Periodicity
import json

@pytest.fixture
def db():
    """Create a temporary database for testing"""
    db = DatabaseHandler("test_habits.json")
    yield db
    # Cleanup after tests
    Path("test_habits.json").unlink(missing_ok=True)

def test_add_habit(db):
    """Test adding a habit to the database"""
    habit = Habit("Test Habit", "Test Description", Periodicity.DAILY)
    db.add_habit(habit)

    assert len(db.habits) == 1
    assert db.habits[0].name == "Test Habit"

    # Verify it was saved to file
    with open("test_habits.json", 'r') as f:
        data = json.load(f)
        assert len(data) == 1
        assert data[0]["name"] == "Test Habit"

def test_remove_habit(db):
    """Test removing a habit from the database"""
    habit = Habit("Test Habit", "Test Description", Periodicity.DAILY)
    db.add_habit(habit)

    assert db.remove_habit("Test Habit") == True
    assert len(db.habits) == 0

def test_get_habits_by_periodicity(db):
    """Test filtering habits by periodicity"""
    daily_habit = Habit("Daily Habit", "Daily", Periodicity.DAILY)
    weekly_habit = Habit("Weekly Habit", "Weekly", Periodicity.WEEKLY)

    db.add_habit(daily_habit)
    db.add_habit(weekly_habit)

    daily_habits = db.get_habits_by_periodicity(Periodicity.DAILY)
    assert len(daily_habits) == 1
    assert daily_habits[0].name == "Daily Habit"