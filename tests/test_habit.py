# tests/test_habit.py

import pytest
from datetime import datetime, timedelta
from src.habit import Habit, Periodicity

def test_habit_creation():
    """Test that a habit can be created with proper attributes"""
    habit = Habit("Exercise", "Daily workout routine", Periodicity.DAILY)

    assert habit.name == "Exercise"
    assert habit.description == "Daily workout routine"
    assert habit.periodicity == Periodicity.DAILY
    assert isinstance(habit.created_at, datetime)
    assert habit.checkoffs == []

def test_habit_checkoff():
    """Test that a habit can be checked off"""
    habit = Habit("Exercise", "Daily workout routine", Periodicity.DAILY)
    habit.check_off()

    assert len(habit.checkoffs) == 1
    assert isinstance(habit.checkoffs[0], datetime)