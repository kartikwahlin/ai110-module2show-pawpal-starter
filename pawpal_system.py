from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Task:
    name: str
    duration: int
    priority: int
    time: str = "08:00"
    frequency: str = "daily"
    due_date: date = field(default_factory=date.today)
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


@dataclass
class Pet:
    name: str
    tasks: list[Task] = field(default_factory=list)


class Owner:
    def __init__(self, name: str, day_start: int, day_end: int):
        self.name = name
        self.day_start = day_start  # hour in 24h format, e.g. 8 = 8:00am
        self.day_end = day_end      # hour in 24h format, e.g. 22 = 10:00pm
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list of pets."""
        self.pets.append(pet)

    def remove_pet(self, pet: Pet) -> None:
        """Remove a pet from this owner's list of pets."""
        self.pets.remove(pet)

    def get_all_tasks(self) -> list[tuple[str, Task]]:
        """Return all tasks across all pets as (pet_name, task) tuples."""
        return [(pet.name, task) for pet in self.pets for task in pet.tasks]


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def mark_task_complete(self, pet_name: str, task: Task) -> None:
        """Mark a task complete and schedule the next occurrence if it is recurring."""
        task.mark_complete()
        delta = {"daily": timedelta(days=1), "weekly": timedelta(weeks=1)}.get(task.frequency)
        if delta:
            pet = next(p for p in self.owner.pets if p.name == pet_name)
            pet.tasks.append(Task(
                name=task.name,
                duration=task.duration,
                priority=task.priority,
                time=task.time,
                frequency=task.frequency,
                due_date=task.due_date + delta,
            ))

    def detect_conflicts(self) -> list[str]:
        """Return a list of warning messages for tasks scheduled at the same time."""
        seen = {}
        warnings = []
        for pet_name, task in self.get_tasks():
            key = (pet_name, task.time)
            if key in seen:
                warnings.append(f"Conflict: [{pet_name}] has two tasks at {task.time} — '{seen[key]}' and '{task.name}'")
            else:
                seen[key] = task.name
        return warnings

    def filter_tasks_completion(self, completed: bool) -> list[tuple[str, Task]]:
        """Return tasks filtered by completion status."""
        return [(pet_name, task) for pet_name, task in self.get_tasks() if task.completed == completed]

    def filter_tasks_by_pet(self, pet_name: str) -> list[tuple[str, Task]]:
        """Return tasks belonging to a specific pet."""
        return [(pname, task) for pname, task in self.get_tasks() if pname == pet_name]

    def get_tasks(self) -> list[tuple[str, Task]]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_tasks(self) -> list[tuple[str, Task]]:
        """Return all tasks sorted by priority in ascending order."""
        tasks = self.get_tasks()
        return sorted(tasks, key=lambda t: t[1].priority)

    def sort_by_time(self, tasks: list[tuple[str, Task]]) -> list[tuple[str, Task]]:
        """Return tasks sorted by their time attribute in HH:MM ascending order, printing any conflicts."""
        for warning in self.detect_conflicts():
            print(warning)
        return sorted(tasks, key=lambda entry: entry[1].time)

