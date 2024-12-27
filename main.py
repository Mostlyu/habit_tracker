# src/main.py

from database import DatabaseHandler
from habit import Habit, Periodicity
from datetime import datetime

class HabitTracker:
    """Main application class for the habit tracker"""

    def __init__(self):
        self.db = DatabaseHandler()
        # Create predefined habits if none exist
        if not self.db.habits:
            self.db.create_predefined_habits()

    def display_menu(self):
        """Display the main menu options"""
        print("\n=== Habit Tracker ===")
        print("1. View all habits")
        print("2. Add new habit")
        print("3. Check off habit")
        print("4. View habit details")
        print("5. View habits by periodicity")
        print("6. Remove habit")
        print("7. Exit")
        return input("Choose an option (1-7): ")

    def run(self):
        """Main application loop"""
        while True:
            choice = self.display_menu()

            if choice == "1":
                self.view_all_habits()
            elif choice == "2":
                self.add_habit()
            elif choice == "3":
                self.check_off_habit()
            elif choice == "4":
                self.view_habit_details()
            elif choice == "5":
                self.view_habits_by_periodicity()
            elif choice == "6":
                self.remove_habit()
            elif choice == "7":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def view_all_habits(self):
        """Display all habits"""
        print("\n=== All Habits ===")
        if not self.db.habits:
            print("No habits found.")
            return

        for habit in self.db.habits:
            status = "✓" if habit.is_completed_for_period() else "✗"
            print(f"{status} {habit.name} ({habit.periodicity.value})")

    def add_habit(self):
        """Add a new habit"""
        print("\n=== Add New Habit ===")
        name = input("Enter habit name: ")

        # Check if habit already exists
        if self.db.get_habit(name):
            print("A habit with this name already exists.")
            return

        description = input("Enter habit description: ")

        print("\nSelect periodicity:")
        print("1. Daily")
        print("2. Weekly")
        period_choice = input("Choose (1-2): ")

        if period_choice == "1":
            periodicity = Periodicity.DAILY
        elif period_choice == "2":
            periodicity = Periodicity.WEEKLY
        else:
            print("Invalid choice. Habit not created.")
            return

        habit = Habit(name, description, periodicity)
        self.db.add_habit(habit)
        print(f"Habit '{name}' created successfully!")

    def check_off_habit(self):
        """Mark a habit as completed"""
        print("\n=== Check Off Habit ===")
        self.view_all_habits()

        if not self.db.habits:
            return

        name = input("\nEnter habit name to check off: ")
        habit = self.db.get_habit(name)

        if habit:
            habit.check_off()
            self.db.save_habits()
            print(f"Habit '{name}' checked off!")
        else:
            print("Habit not found.")

    def view_habit_details(self):
        """View detailed information about a specific habit"""
        print("\n=== Habit Details ===")
        name = input("Enter habit name: ")
        habit = self.db.get_habit(name)

        if habit:
            print(f"\nName: {habit.name}")
            print(f"Description: {habit.description}")
            print(f"Periodicity: {habit.periodicity.value}")
            print(f"Created: {habit.created_at.strftime('%Y-%m-%d')}")
            print(f"Current streak: {habit.get_current_streak()} {habit.periodicity.value} periods")
            print(f"Completed this period: {'Yes' if habit.is_completed_for_period() else 'No'}")
        else:
            print("Habit not found.")

    def view_habits_by_periodicity(self):
        """View habits filtered by periodicity"""
        print("\n=== View Habits by Periodicity ===")
        print("1. Daily habits")
        print("2. Weekly habits")
        choice = input("Choose (1-2): ")

        if choice == "1":
            habits = self.db.get_habits_by_periodicity(Periodicity.DAILY)
            print("\n=== Daily Habits ===")
        elif choice == "2":
            habits = self.db.get_habits_by_periodicity(Periodicity.WEEKLY)
            print("\n=== Weekly Habits ===")
        else:
            print("Invalid choice.")
            return

        if not habits:
            print("No habits found.")
            return

        for habit in habits:
            status = "✓" if habit.is_completed_for_period() else "✗"
            print(f"{status} {habit.name}")

    def remove_habit(self):
        """Remove a habit"""
        print("\n=== Remove Habit ===")
        self.view_all_habits()

        if not self.db.habits:
            return

        name = input("\nEnter habit name to remove: ")
        if self.db.remove_habit(name):
            print(f"Habit '{name}' removed successfully!")
        else:
            print("Habit not found.")

if __name__ == "__main__":
    app = HabitTracker()
    app.run()