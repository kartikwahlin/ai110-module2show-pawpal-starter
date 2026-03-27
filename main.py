from pawpal_system import Task, Pet, Owner, Scheduler

owner = Owner(name="Alex", day_start=8, day_end=22)

dog = Pet(name="Buddy")
cat = Pet(name="Whiskers")

owner.add_pet(dog)
owner.add_pet(cat)

# Tasks added out of order intentionally
task1 = Task("Walk", 30, 3, time="14:00")
task1half = Task("Walkdouble", 30, 3, time="14:00")
task2 = Task("Feed", 5, 1, time="08:00")
dog.tasks.extend([task1, task2, task1half])

task3 = Task("Feed cat food", 5, 1, time="09:00")
cat.tasks.append(task3)

scheduler = Scheduler(owner)

print("Today's Schedule (sorted by time)")
print("-----------------------------------")
for pet_name, task in scheduler.sort_by_time(scheduler.get_tasks()):
    print(f"{task.time} - [{pet_name}] {task.name}")

print("\nBuddy's Tasks Only")
print("------------------")
for pet_name, task in scheduler.filter_tasks_by_pet("Buddy"):
    print(f"[{pet_name}] {task.name} at {task.time}")

print("\nIncomplete Tasks")
print("----------------")
for pet_name, task in scheduler.filter_tasks_completion(completed=False):
    print(f"[{pet_name}] {task.name}")
