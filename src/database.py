# src/database.py

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Optional
from .habit import Habit, Periodicity

class DatabaseHandler:
    """
    Handles persistence of habits to and from JSON file storage.

    Attributes:
        db_file (Path): Path to the JSON file storing habits
        habits (list[Habit]): List of tracked habits
    """

    def __init__(self, db_file: str = "habits.json"):
        """
        Initialize database handler with file path

        Args:
            db_file (str): Name of the JSON file to store habits
        """
        self.db_file = Path(db_file)
        self.habits: List[Habit] = []
        self._load_habits()

    def _load_habits(self) -> None:
        """Load habits from JSON file if it exists"""
        try:
            if self.db_file.exists():
                with open(self.db_file, 'r') as f:
                    habits_data = json.load(f)
                    self.habits = [Habit.from_dict(habit_data)
                                 for habit_data in habits_data]
        except json.JSONDecodeError:
            print(f"Error reading {self.db_file}. Starting with empty habits list.")
            self.habits = []

    def save_habits(self) -> None:
        """Save current habits to JSON file"""
        habits_data = [habit.to_dict() for habit in self.habits]
        with open(self.db_file, 'w') as f:
            json.dump(habits_data, f, indent=2)

    def add_habit(self, habit: Habit) -> None:
        """
        Add a new habit to the database

        Args:
            habit (Habit): The habit to add
        """
        self.habits.append(habit)
        self.save_habits()

    def remove_habit(self, habit_name: str) -> bool:
        """
        Remove a habit from the database

        Args:
            habit_name (str): Name of the habit to remove

        Returns:
            bool: True if habit was removed, False if not found
        """
        initial_length = len(self.habits)
        self.habits = [h for h in self.habits if h.name != habit_name]

        if len(self.habits) < initial_length:
            self.save_habits()
            return True
        return False

    def get_habit(self, habit_name: str) -> Optional[Habit]:
        """
        Get a habit by name

        Args:
            habit_name (str): Name of the habit to find

        Returns:
            Optional[Habit]: The habit if found, None otherwise
        """
        for habit in self.habits:
            if habit.name == habit_name:
                return habit
        return None

    def get_habits_by_periodicity(self, periodicity: Periodicity) -> List[Habit]:
        """
        Get all habits with a specific periodicity

        Args:
            periodicity (Periodicity): The periodicity to filter by

        Returns:
            List[Habit]: List of habits with the specified periodicity
        """
        return [h for h in self.habits if h.periodicity == periodicity]

    def create_predefined_habits(self) -> None:
        """Create predefined habits if no habits exist"""
        if not self.habits:
            predefined = [
                Habit("Morning Exercise",
                      "15 minutes of morning workout",
                      Periodicity.DAILY),
                Habit("Read",
                      "Read for 30 minutes",
                      Periodicity.DAILY),
                Habit("Meditate",
                      "10 minutes mindfulness meditation",
                      Periodicity.DAILY),
                Habit("Weekly Planning",
                      "Plan goals and tasks for the week",
                      Periodicity.WEEKLY),
                Habit("House Cleaning",
                      "Deep clean the house",
                      Periodicity.WEEKLY)
            ]

            # Add some example tracking data for the past 4 weeks
            current_date = datetime.now()
            for habit in predefined:
                # Add checkoffs for the past 28 days
                for i in range(28):
                    if habit.periodicity == Periodicity.DAILY:
                        # Add daily checkoff
                        habit.checkoffs.append(
                            current_date - timedelta(days=i)
                        )
                    elif habit.periodicity == Periodicity.WEEKLY and i % 7 == 0:
                        # Add weekly checkoff
                        habit.checkoffs.append(
                            current_date - timedelta(days=i)
                        )

                self.add_habit(habit)