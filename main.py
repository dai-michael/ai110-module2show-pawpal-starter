from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Jordan", available_minutes=90, preferred_start_time="08:00", priority_preference="high")

mochi = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
mochi.add_task(Task(description="Morning walk", duration_minutes=30, priority="high", frequency="daily"))
mochi.add_task(Task(description="Feeding", duration_minutes=10, priority="high", frequency="daily"))

biscuit = Pet(name="Biscuit", species="cat", age=5, breed="Tabby")
biscuit.add_task(Task(description="Litter box cleaning", duration_minutes=5, priority="medium", frequency="daily"))

owner.add_pet(mochi)
owner.add_pet(biscuit)

scheduler = Scheduler(date="2026-07-03")
scheduler.generate(owner)

print("Today's Schedule")
print(scheduler.explain())
