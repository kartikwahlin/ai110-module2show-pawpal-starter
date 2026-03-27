from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_scheduler(*pets):
    owner = Owner(name="Alex", day_start=8, day_end=22)
    for pet in pets:
        owner.add_pet(pet)
    return Scheduler(owner)


# ---------------------------------------------------------------------------
# Existing tests
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Recurrence / task timing
# ---------------------------------------------------------------------------

def test_mark_task_complete_creates_daily_followup():
    """Completing a daily task should schedule a new task one day later."""
    today = date.today()
    task = Task(name="Feed", duration=5, priority=1, frequency="daily", due_date=today)
    pet = Pet(name="Buddy", tasks=[task])
    scheduler = make_scheduler(pet)

    scheduler.mark_task_complete("Buddy", task)

    assert task.completed is True
    # One new task should have been appended
    assert len(pet.tasks) == 2
    followup = pet.tasks[1]
    assert followup.due_date == today + timedelta(days=1)
    assert followup.completed is False


def test_mark_task_complete_creates_weekly_followup():
    """Completing a weekly task should schedule a new task seven days later."""
    today = date.today()
    task = Task(name="Groom", duration=20, priority=2, frequency="weekly", due_date=today)
    pet = Pet(name="Luna", tasks=[task])
    scheduler = make_scheduler(pet)

    scheduler.mark_task_complete("Luna", task)

    assert len(pet.tasks) == 2
    followup = pet.tasks[1]
    assert followup.due_date == today + timedelta(weeks=1)


def test_mark_task_complete_no_followup_for_one_time():
    """A task with an unrecognised frequency should not create a follow-up."""
    task = Task(name="Vet visit", duration=60, priority=1, frequency="once")
    pet = Pet(name="Milo", tasks=[task])
    scheduler = make_scheduler(pet)

    scheduler.mark_task_complete("Milo", task)

    # Still only the original (now completed) task
    assert len(pet.tasks) == 1
    assert task.completed is True


def test_followup_inherits_task_properties():
    """The rescheduled task should keep the same name, duration, priority, and time."""
    today = date.today()
    task = Task(name="Walk", duration=30, priority=3, time="07:30", frequency="daily", due_date=today)
    pet = Pet(name="Rex", tasks=[task])
    scheduler = make_scheduler(pet)

    scheduler.mark_task_complete("Rex", task)

    followup = pet.tasks[1]
    assert followup.name == "Walk"
    assert followup.duration == 30
    assert followup.priority == 3
    assert followup.time == "07:30"
    assert followup.frequency == "daily"


# ---------------------------------------------------------------------------
# Conflict detection
# ---------------------------------------------------------------------------

def test_no_conflicts_when_no_tasks():
    """A scheduler with no tasks should report zero conflicts."""
    scheduler = make_scheduler()
    assert scheduler.detect_conflicts() == []


def test_no_conflicts_different_times():
    """Tasks for the same pet at different times should not conflict."""
    pet = Pet(name="Buddy", tasks=[
        Task(name="Walk", duration=30, priority=1, time="08:00"),
        Task(name="Feed", duration=5,  priority=2, time="09:00"),
    ])
    scheduler = make_scheduler(pet)
    assert scheduler.detect_conflicts() == []


def test_conflict_same_pet_same_time():
    """Two tasks for the same pet at the same time should produce one conflict warning."""
    pet = Pet(name="Buddy", tasks=[
        Task(name="Walk", duration=30, priority=1, time="08:00"),
        Task(name="Feed", duration=5,  priority=2, time="08:00"),
    ])
    scheduler = make_scheduler(pet)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1
    assert "Buddy" in conflicts[0]
    assert "08:00" in conflicts[0]


def test_no_conflict_different_pets_same_time():
    """The same time slot is only a conflict when it belongs to the same pet."""
    pet1 = Pet(name="Buddy", tasks=[Task(name="Walk", duration=30, priority=1, time="08:00")])
    pet2 = Pet(name="Luna",  tasks=[Task(name="Feed", duration=5,  priority=1, time="08:00")])
    scheduler = make_scheduler(pet1, pet2)
    assert scheduler.detect_conflicts() == []


def test_three_tasks_same_pet_same_time():
    """Three tasks at the same time for one pet should generate two conflict warnings."""
    pet = Pet(name="Buddy", tasks=[
        Task(name="Walk",  duration=30, priority=1, time="08:00"),
        Task(name="Feed",  duration=5,  priority=2, time="08:00"),
        Task(name="Brush", duration=10, priority=3, time="08:00"),
    ])
    scheduler = make_scheduler(pet)
    conflicts = scheduler.detect_conflicts()
    # Second and third task each conflict with the first
    assert len(conflicts) == 2


# ---------------------------------------------------------------------------
# Sorting and filtering
# ---------------------------------------------------------------------------

def test_organize_tasks_sorts_by_priority():
    """organize_tasks should return tasks in ascending priority order."""
    pet = Pet(name="Buddy", tasks=[
        Task(name="Bath",  duration=20, priority=3),
        Task(name="Walk",  duration=30, priority=1),
        Task(name="Feed",  duration=5,  priority=2),
    ])
    scheduler = make_scheduler(pet)
    ordered = scheduler.organize_tasks()
    priorities = [t.priority for _, t in ordered]
    assert priorities == sorted(priorities)


def test_sort_by_time_returns_ascending_order():
    """sort_by_time should return tasks ordered earliest to latest."""
    pet = Pet(name="Buddy", tasks=[
        Task(name="Feed",  duration=5,  priority=1, time="10:00"),
        Task(name="Walk",  duration=30, priority=2, time="07:00"),
        Task(name="Brush", duration=10, priority=3, time="08:30"),
    ])
    scheduler = make_scheduler(pet)
    sorted_tasks = scheduler.sort_by_time(scheduler.get_tasks())
    times = [t.time for _, t in sorted_tasks]
    assert times == sorted(times)


def test_filter_tasks_completion_incomplete():
    """filter_tasks_completion(False) should return only incomplete tasks."""
    task_done = Task(name="Walk", duration=30, priority=1)
    task_done.completed = True
    task_pending = Task(name="Feed", duration=5, priority=2)
    pet = Pet(name="Buddy", tasks=[task_done, task_pending])
    scheduler = make_scheduler(pet)

    incomplete = scheduler.filter_tasks_completion(False)
    assert all(not t.completed for _, t in incomplete)
    assert len(incomplete) == 1
    assert incomplete[0][1].name == "Feed"


def test_filter_tasks_completion_complete():
    """filter_tasks_completion(True) should return only completed tasks."""
    task_done = Task(name="Walk", duration=30, priority=1)
    task_done.completed = True
    task_pending = Task(name="Feed", duration=5, priority=2)
    pet = Pet(name="Buddy", tasks=[task_done, task_pending])
    scheduler = make_scheduler(pet)

    done = scheduler.filter_tasks_completion(True)
    assert all(t.completed for _, t in done)
    assert len(done) == 1
    assert done[0][1].name == "Walk"


def test_filter_tasks_by_pet():
    """filter_tasks_by_pet should return only tasks belonging to the named pet."""
    pet1 = Pet(name="Buddy", tasks=[Task(name="Walk", duration=30, priority=1)])
    pet2 = Pet(name="Luna",  tasks=[Task(name="Feed", duration=5,  priority=1)])
    scheduler = make_scheduler(pet1, pet2)

    buddy_tasks = scheduler.filter_tasks_by_pet("Buddy")
    assert len(buddy_tasks) == 1
    assert buddy_tasks[0][0] == "Buddy"

    luna_tasks = scheduler.filter_tasks_by_pet("Luna")
    assert len(luna_tasks) == 1
    assert luna_tasks[0][0] == "Luna"
