from pawpal_system import Owner, Pet, Scheduler, Task


def _task(description, duration_minutes, priority="medium", frequency="once", scheduled_time=None, date=None):
    return Task(
        description=description,
        duration_minutes=duration_minutes,
        priority=priority,
        frequency=frequency,
        scheduled_time=scheduled_time,
        date=date,
    )


# --- Sorting correctness ---------------------------------------------------

def test_get_schedule_returns_tasks_in_chronological_order():
    scheduler = Scheduler(date="2026-07-05")

    afternoon = _task("Walk", 30, scheduled_time="14:00")
    morning = _task("Feeding", 10, scheduled_time="07:00")
    midday = _task("Playtime", 20, scheduled_time="12:00")

    # Appended out of order; get_schedule() must not depend on insertion order.
    scheduler.scheduled_tasks = [afternoon, morning, midday]

    ordered = scheduler.get_schedule()

    assert [t.description for t in ordered] == ["Feeding", "Playtime", "Walk"]


def test_get_schedule_places_unscheduled_tasks_first():
    scheduler = Scheduler(date="2026-07-05")

    scheduled = _task("Walk", 30, scheduled_time="09:00")
    unscheduled = _task("Grooming", 15, scheduled_time=None)

    scheduler.scheduled_tasks = [scheduled, unscheduled]

    ordered = scheduler.get_schedule()

    assert ordered[0] is unscheduled
    assert ordered[1] is scheduled


# --- Recurrence logic -------------------------------------------------------

def test_mark_daily_task_complete_creates_task_for_the_following_day():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
    task = _task("Morning walk", 30, frequency="daily", scheduled_time="08:00", date="2026-07-05")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.date == "2026-07-06"
    assert next_task.completed is False
    assert next_task.scheduled_time is None
    assert next_task in pet.get_tasks()


def test_mark_weekly_task_complete_creates_task_seven_days_later():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
    task = _task("Nail trim", 15, frequency="weekly", date="2026-07-05")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task.date == "2026-07-12"


def test_mark_non_recurring_task_complete_creates_no_new_task():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
    task = _task("Vet visit", 45, frequency="once", date="2026-07-05")
    pet.add_task(task)

    next_task = task.mark_complete()

    assert next_task is None
    assert len(pet.get_tasks()) == 1


def test_mark_complete_without_pet_does_not_raise_and_returns_next_task():
    task = _task("Morning walk", 30, frequency="daily", date="2026-07-05")

    next_task = task.mark_complete()

    assert next_task is not None
    assert next_task.date == "2026-07-06"


# --- Conflict detection ------------------------------------------------------

def test_find_conflicts_flags_tasks_at_duplicate_start_time():
    scheduler = Scheduler(date="2026-07-05")

    task_a = _task("Walk", 30, scheduled_time="09:00")
    task_a.pet_name = "Mochi"
    task_b = _task("Grooming", 20, scheduled_time="09:00")
    task_b.pet_name = "Biscuit"

    scheduler.scheduled_tasks = [task_a, task_b]
    conflicts = scheduler.find_conflicts()

    assert len(conflicts) == 1
    assert {task_a, task_b} == set(conflicts[0])


def test_find_conflicts_flags_overlapping_but_not_identical_times():
    scheduler = Scheduler(date="2026-07-05")

    task_a = _task("Walk", 30, scheduled_time="09:00")  # 09:00-09:30
    task_b = _task("Grooming", 30, scheduled_time="09:15")  # 09:15-09:45

    scheduler.scheduled_tasks = [task_a, task_b]

    assert len(scheduler.find_conflicts()) == 1


def test_find_conflicts_does_not_flag_back_to_back_tasks():
    scheduler = Scheduler(date="2026-07-05")

    task_a = _task("Walk", 30, scheduled_time="09:00")  # ends 09:30
    task_b = _task("Grooming", 20, scheduled_time="09:30")  # starts right after

    scheduler.scheduled_tasks = [task_a, task_b]

    assert scheduler.find_conflicts() == []


def test_generate_produces_no_conflicts_for_back_to_back_priority_packing():
    owner = Owner(name="Jamie", available_minutes=120, preferred_start_time="08:00", priority_preference="high")
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
    owner.add_pet(pet)

    pet.add_task(_task("Walk", 30, priority="high"))
    pet.add_task(_task("Feeding", 15, priority="medium"))
    pet.add_task(_task("Playtime", 20, priority="low"))

    scheduler = Scheduler(date="2026-07-05")
    scheduler.generate(owner)

    assert scheduler.conflicts == []