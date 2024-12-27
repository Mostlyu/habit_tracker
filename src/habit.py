# src/habit.py

from datetime import datetime, timedelta
from enum import Enum

class Periodicity(Enum):
    """Enum for habit periodicity types"""
    DAILY = "daily"
    WEEKLY = "weekly"

class Habit:
    """
    A class to represent a habit to be tracked.

    Attributes:
        name (str): The name of the habit
        description (str): A description of the habit
        periodicity (Periodicity): How often the habit should be performed
        created_at (datetime): When the habit was created
        checkoffs (list): List of datetime objects when the habit was completed
    """

    def __init__(self, name: str, description: str, periodicity: Periodicity):
        self.name = name
        self.description = description
        self.periodicity = periodicity
        self.created_at = datetime.now()
        self.checkoffs = []

    def check_off(self) -> None:
        """Mark the habit as complete for the current time"""
        self.checkoffs.append(datetime.now())

    def is_completed_for_period(self) -> bool:
        """Check if the habit has been completed for the current period"""
        if not self.checkoffs:
            return False

        latest_checkoff = max(self.checkoffs)
        current_time = datetime.now()

        if self.periodicity == Periodicity.DAILY:
            # Check if the habit was completed today
            return latest_checkoff.date() == current_time.date()
        else:  # WEEKLY
            # Check if the habit was completed this week
            week_start = current_time - timedelta(days=current_time.weekday())
            return latest_checkoff >= week_start

    def get_current_streak(self) -> int:
        """Calculate the current streak for this habit"""
        # We'll implement this later as it's more complex
        pass

    def to_dict(self) -> dict:
        """Convert the habit to a dictionary for storage"""
        return {
            "name": self.name,
            "description": self.description,
            "periodicity": self.periodicity.value,
            "created_at": self.created_at.isoformat(),
            "checkoffs": [dt.isoformat() for dt in self.checkoffs]
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Habit':
        """Create a habit instance from a dictionary"""
        habit = cls(
            name=data["name"],
            description=data["description"],
            periodicity=Periodicity(data["periodicity"])
        )
        habit.created_at = datetime.fromisoformat(data["created_at"])
        habit.checkoffs = [datetime.fromisoformat(dt) for dt in data["checkoffs"]]
        return habit