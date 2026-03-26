from pawpal_system import Task, Pet


def test_mark_complete():
    task = Task(name="Walk", duration=30, priority=1)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_count():
    pet = Pet(name="Buddy")
    task = Task(name="Feed", duration=5, priority=1)
    assert len(pet.tasks) == 0
    pet.tasks.append(task)
    assert len(pet.tasks) == 1
