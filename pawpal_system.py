from datetime import datetime, timedelta
from typing import List, Optional, Tuple

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
TIME_FORMAT = "%H:%M"


class Task:
    RECURRING_FREQUENCIES = ("daily", "weekly")

    def __init__(self, description: str, duration_minutes: int, priority: str, frequency: str,
                 scheduled_time: Optional[str] = None, completed: bool = False, pet_name: Optional[str] = None):
        self.description = description
        self.duration_minutes = duration_minutes
        self.priority = priority
        self.frequency = frequency
        self.scheduled_time = scheduled_time
        self.completed = completed
        self.pet_name = pet_name
        self._pet: Optional["Pet"] = None

    def next_occurrence(self) -> Optional["Task"]:
        """Build the next instance of this task if its frequency recurs.

        Only "daily" and "weekly" tasks recur (see RECURRING_FREQUENCIES); anything
        else (e.g. "monthly", one-off tasks) returns None.

        Returns:
            A new, unscheduled, incomplete Task cloned from this one, or None if
            this task's frequency does not recur.
        """
        if self.frequency not in self.RECURRING_FREQUENCIES:
            return None
        return Task(
            description=self.description,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            pet_name=self.pet_name,
        )

    def mark_complete(self) -> Optional["Task"]:
        """Mark this task as completed and roll it forward if it recurs.

        If this task recurs (see next_occurrence), the new instance is
        automatically appended to the owning pet's task list, so recurring
        tasks keep reappearing on future schedules without manual re-entry.

        Returns:
            The newly spawned next-occurrence Task, or None if this task
            doesn't recur or isn't attached to a Pet yet.
        """
        self.completed = True
        next_task = self.next_occurrence()
        if next_task is not None and self._pet is not None:
            self._pet.add_task(next_task)
        return next_task

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
        task._pet = self
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

    def filter_tasks(self, pet_name: Optional[str] = None, completed: Optional[bool] = None) -> List[Task]:
        """Return tasks across all pets, narrowed by pet name and/or completion status.

        Filters are combined with AND and applied only when provided, so
        omitting both args returns every task (same as get_all_tasks()).

        Args:
            pet_name: Only include tasks belonging to the pet with this name.
            completed: Only include tasks whose completed status matches this value.

        Returns:
            The matching tasks, in the same relative order as get_all_tasks().
        """
        tasks = self.get_all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks


class Scheduler:
    def __init__(self, date: str):
        self.date = date
        self.scheduled_tasks: List[Task] = []
        self.skipped_tasks: List[Task] = []
        self.conflicts: List[Tuple[Task, Task]] = []
        self.total_minutes_used = 0

    def generate(self, owner: Owner) -> None:
        """Greedily schedule the owner's tasks by priority within their available time.

        Tasks are sorted into priority tiers (high, medium, low) and packed
        back-to-back starting at the owner's preferred start time. A task is
        skipped rather than scheduled once it would push total scheduled
        minutes past owner.available_minutes; scheduling then continues with
        the remaining tasks, since a later, shorter task may still fit.

        This is a greedy, priority-first strategy rather than an optimal
        packing (e.g. knapsack): a single high-priority task is never
        skipped in favor of several lower-priority tasks that would pack
        more efficiently, even though that can waste leftover minutes.

        Populates scheduled_tasks, skipped_tasks, total_minutes_used, and
        conflicts (via find_conflicts) as a side effect.

        Args:
            owner: The owner whose pets' tasks should be scheduled.
        """
        self.scheduled_tasks = []
        self.skipped_tasks = []
        self.total_minutes_used = 0

        tasks = sorted(
            owner.get_all_tasks(),
            key=lambda t: PRIORITY_ORDER.get(t.priority, len(PRIORITY_ORDER)),
        )

        cursor = datetime.strptime(owner.preferred_start_time, TIME_FORMAT)

        for task in tasks:
            if self.total_minutes_used + task.duration_minutes > owner.available_minutes:
                self.skipped_tasks.append(task)
                continue

            task.schedule(cursor.strftime(TIME_FORMAT))
            self.scheduled_tasks.append(task)
            self.total_minutes_used += task.duration_minutes

            cursor += timedelta(minutes=task.duration_minutes)

        self.conflicts = self.find_conflicts()

    def find_conflicts(self) -> List[Tuple[Task, Task]]:
        """Detect scheduled tasks whose time ranges overlap, regardless of which pet they belong to.

        Checks every pair of scheduled tasks (O(n^2), fine at the scale of a
        day's task list), since an owner can only be in one place at a time
        no matter which pet a task is for. generate()'s own back-to-back
        packing never produces overlaps on its own; this exists to catch
        overlaps introduced by manually re-scheduling tasks (e.g. pinning a
        fixed-time appointment).

        Returns:
            A list of (task_a, task_b) pairs whose time ranges overlap.
        """
        conflicts = []
        tasks = [t for t in self.scheduled_tasks if t.scheduled_time is not None]
        for i in range(len(tasks)):
            for j in range(i + 1, len(tasks)):
                if self._times_overlap(tasks[i], tasks[j]):
                    conflicts.append((tasks[i], tasks[j]))
        return conflicts

    @staticmethod
    def _times_overlap(a: Task, b: Task) -> bool:
        """Check whether two scheduled tasks' time ranges intersect.

        Treats each task's span as the half-open interval
        [scheduled_time, end_time()), so a task ending exactly when another
        starts does not count as overlapping.

        Args:
            a: First task; must have a scheduled_time set.
            b: Second task; must have a scheduled_time set.

        Returns:
            True if a and b occupy any overlapping time.
        """
        return a.scheduled_time < b.end_time() and b.scheduled_time < a.end_time()

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

        if self.conflicts:
            lines.append("Conflicts (overlapping times):")
            for task_a, task_b in self.conflicts:
                lines.append(
                    f"  - {task_a.pet_name}: {task_a.description} ({task_a.scheduled_time}-{task_a.end_time()}) "
                    f"overlaps {task_b.pet_name}: {task_b.description} ({task_b.scheduled_time}-{task_b.end_time()})"
                )

        return "\n".join(lines)

    def get_schedule(self) -> List[Task]:
        """Return the scheduled tasks sorted by their scheduled time."""
        return sorted(self.scheduled_tasks, key=lambda t: t.scheduled_time or "")
