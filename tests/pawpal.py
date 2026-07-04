from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task(description="Morning walk", duration_minutes=30, priority="high", frequency="daily")
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="dog", age=3, breed="Shiba Inu")
    assert len(pet.get_tasks()) == 0

    pet.add_task(Task(description="Feeding", duration_minutes=10, priority="high", frequency="daily"))

    assert len(pet.get_tasks()) == 1