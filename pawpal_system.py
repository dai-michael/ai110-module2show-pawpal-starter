from datetime import datetime, timedelta
from typing import List, Optional

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
TIME_FORMAT = "%H:%M"


class Task:
    def __init__(self, description: str, duration_minutes: int, priority: str, frequency: str,
                 scheduled_time: Optional[str] = None, completed: bool = False, pet_name: Optional[str] = None):
        self.description = description
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency
        self.scheduled_time = scheduled_time
        self.completed = completed
        self.pet_name = pet_name

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def mark_incomplete(self) -> None:
        """Mark this task as not completed."""
        self.completed = False

    def end_time(self) -> Optional[str]:
        """Return the task's end time based on its scheduled time and duration."""
        if self.scheduled_time is None:
            return None
        start = datetime.strptime(self.scheduled_time, TIME_FORMAT)
        end = start + timedelta(minutes=self.duration_minutes)
        return end.strftime(TIME_FORMAT)

    def schedule(self, start_time: str) -> None:
        """Set the task's scheduled start time."""
        self.scheduled_time = start_time


class Pet:
    def __init__(self, name: str, species: str, age: int, breed: str):
        self.name = name
        self.species = species
        self.age = age
        self.breed = breed
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> None:
        """Add a task to this pet's task list, tagging it with this pet's name."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, description: str) -> None:
        """Remove any tasks matching the given description."""
        self.tasks = [t for t in self.tasks if t.description != description]

    def get_tasks(self) -> List[Task]:
        """Return a copy of this pet's task list."""
        return list(self.tasks)


class Owner:
    def __init__(self, name: str, available_minutes: int, preferred_start_time: str, priority_preference: str):
        self.name = name
        self.pets: List[Pet] = []
        self.available_minutes = available_minutes
        self.preferred_start_time = preferred_start_time
        self.priority_preference = priority_preference

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, name: str) -> None:
        """Remove any pets matching the given name."""
        self.pets = [p for p in self.pets if p.name != name]

    def get_pets(self) -> List[Pet]:
        """Return a copy of this owner's pet list."""
        return list(self.pets)

    def get_all_tasks(self) -> List[Task]:
        """Return every task across all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks


class Scheduler:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.total_minutes_used = 0

    def generate(self, owner: Owner) -> None:
        """Greedily schedule the owner's tasks by priority within their available time."""
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.total_minutes_used = 0

        tasks = sorted(
            owner.get_all_tasks(),
            key=lambda t: PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)),
        )

        cursor = datetime.strptime(owner.preferred_start_time, TIME_FORMAT)
        minutes_remaining = owner.available_minutes

        for task in tasks:
            if task.duration_minutes > minutes_remaining:
                self.skipped_tasks.append(task)
                continue

            task.schedule(cursor.strftime(TIME_FORMAT))
            self.scheduled_tasks.append(task)
            self.total_minutes_used += task.duration_minutes

            cursor += timedelta(minutes=task.duration_minutes)
            minutes_remaining -= task.duration_minutes

    def explain(self) -> str:
        """Return a human-readable summary of the scheduled and skipped tasks."""
        if not self.scheduled_tasks:
            return f"No tasks scheduled for {self.date}."

        lines = [f"Plan for {self.date}:"]
        for task in self.get_schedule():
            lines.append(
                f"  {task.scheduled_time}-{task.end_time()} — {task.pet_name}: {task.description} "
                f"({task.duration_minutes} min) [priority: {task.priority}]"
            )

        if self.skipped_tasks:
            lines.append("Skipped (not enough time available):")
            for task in self.skipped_tasks:
                lines.append(f"  - {task.pet_name}: {task.description} ({task.duration_minutes} min)")

        return "\n".join(lines)

    def get_schedule(self) -> List[Task]:
        """Return the scheduled tasks sorted by their scheduled time."""
        return sorted(self.scheduled_tasks, key=lambda t: t.scheduled_time or "")
