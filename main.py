from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00", priority_preference="high")

mochi = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
# Tasks are added out of priority/time order on purpose to exercise the scheduler's sorting.
mochi.add_task(Task(description="Feeding", duration_minutes=10, priority="high", frequency="daily"))
mochi.add_task(Task(description="Nail trim", duration_minutes=15, priority="low", frequency="weekly", completed=True))
mochi.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", frequency="daily"))
mochi.add_task(Task(description="Brushing", duration_minutes=10, priority="medium", frequency="weekly"))

biscuit = Pet(name="Biscuit", species="cat", age=5, breed="Tabby")
biscuit.add_task(Task(description="Vet checkup", duration_minutes=20, priority="high", frequency="monthly"))
biscuit.add_task(Task(description="Litter box cleaning", duration_minutes=5, priority="medium", frequency="daily"))

owner.add_pet(mochi)
owner.add_pet(biscuit)

scheduler = Scheduler(date="2026-07-03")
scheduler.generate(owner)

print("Today's Schedule")
print(scheduler.explain())

print("\nScheduled tasks sorted by time:")
for task in scheduler.get_schedule():
    print(f"  {task.scheduled_time} — {task.pet_name}: {task.description}")

print("\nIncomplete tasks (filtered):")
for task in owner.filter_tasks(completed=False):
    print(f"  {task.pet_name}: {task.description} [{task.priority}]")

print("\nCompleted tasks (filtered):")
for task in owner.filter_tasks(completed=True):
    print(f"  {task.pet_name}: {task.description} [{task.priority}]")

print(f"\nTasks for {mochi.name} only (filtered):")
for task in owner.filter_tasks(pet_name=mochi.name):
    print(f"  {task.description} [{task.priority}]")

# --- Conflict detection demo ---
# generate() always packs tasks back-to-back, so it can never produce an overlap on its own.
# To exercise find_conflicts(), pin two tasks from different pets to the same time, as if
# they were booked as fixed appointments (e.g. two same-time vet calls).
grooming = Task(description="Grooming appointment", duration_minutes=30, priority="medium", frequency="weekly")
vet_call = Task(description="Vet follow-up call", duration_minutes=15, priority="high", frequency="daily")
mochi.add_task(grooming)
biscuit.add_task(vet_call)

grooming.schedule("10:00")
vet_call.schedule("10:10")
scheduler.scheduled_tasks.extend([grooming, vet_call])
scheduler.conflicts = scheduler.find_conflicts()

print("\nToday's Schedule (with a scheduling conflict introduced)")
print(scheduler.explain())
