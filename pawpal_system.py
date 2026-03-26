from dataclasses import dataclass, field


@dataclass
class Profile:
    owner_name: str
    pet_name: str


@dataclass
class Task:
    name: str
    duration: int   # minutes
    priority: int   # lower number = higher priority


class TaskList:
    def __init__(self):
        self.tasks: list[Task] = []

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, name: str) -> None:
        pass

    def get_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, task_list: TaskList, profile: Profile, time_budget: int):
        self.task_list = task_list
        self.profile = profile
        self.time_budget = time_budget  # minutes available in the day

    def generate_plan(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass
