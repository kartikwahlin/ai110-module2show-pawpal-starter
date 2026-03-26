from dataclasses import dataclass, field


@dataclass
class Task:
    name: str
    duration: int
    priority: int
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

    def get_tasks(self) -> list[tuple[str, Task]]:
        """Retrieve all tasks from the owner's pets."""
        return self.owner.get_all_tasks()

    def organize_tasks(self) -> list[tuple[str, Task]]:
        """Return all tasks sorted by priority in ascending order."""
        tasks = self.get_tasks()
        return sorted(tasks, key=lambda t: t[1].priority)

    def generate_times(self) -> list[tuple[str, str, int]]:
        """Assign start times to tasks in priority order, returning (pet_name, task_name, start_minute) tuples."""
        schedule = []
        current_time = self.owner.day_start * 60
        for pet_name, task in self.organize_tasks():
            schedule.append((pet_name, task.name, current_time))
            current_time += task.duration
        return schedule
