from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs (UI only)")
owner_name = st.text_input("Owner name", value="Jordan")
available_minutes = st.number_input("Available minutes today", min_value=1, max_value=600, value=60)
preferred_start_time = st.time_input("Preferred start time", value=time(8, 0))
priority_preference = st.selectbox("Owner priority preference", ["low", "medium", "high"], index=2)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        name=owner_name,
        available_minutes=int(available_minutes),
        preferred_start_time=preferred_start_time.strftime("%H:%M"),
        priority_preference=priority_preference,
    )
owner = st.session_state.owner
owner.name = owner_name
owner.available_minutes = int(available_minutes)
owner.preferred_start_time = preferred_start_time.strftime("%H:%M")
owner.priority_preference = priority_preference

st.markdown("### Pets")
st.caption("Add one or more pets for this owner.")

with st.form("add_pet_form", clear_on_submit=True):
    new_pet_name = st.text_input("Pet name", value="Mochi")
    new_species = st.selectbox("Species", ["dog", "cat", "other"])
    new_age = st.number_input("Pet age", min_value=0, max_value=30, value=3)
    new_breed = st.text_input("Breed", value="Shiba Inu")
    pet_submitted = st.form_submit_button("Add pet")

if pet_submitted:
    owner.add_pet(Pet(name=new_pet_name, species=new_species, age=int(new_age), breed=new_breed))

if owner.get_pets():
    st.write("Current pets:")
    st.table(
        [{"name": p.name, "species": p.species, "age": p.age, "breed": p.breed} for p in owner.get_pets()]
    )
else:
    st.info("No pets yet. Add one above.")

st.markdown("### Tasks")
st.caption("Add a few tasks for a pet. These feed directly into the scheduler below.")

if not owner.get_pets():
    st.info("Add a pet first before adding tasks.")
else:
    pet_index = st.selectbox(
        "Pet", range(len(owner.get_pets())), format_func=lambda i: owner.get_pets()[i].name
    )
    pet = owner.get_pets()[pet_index]

    col1, col2, col3 = st.columns(3)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

    if st.button("Add task"):
        pet.add_task(
            Task(description=task_title, duration_minutes=int(duration), priority=priority, frequency="daily")
        )

    if pet.get_tasks():
        st.write(f"Current tasks for {pet.name}:")
        st.table(
            [
                {"title": t.description, "duration_minutes": t.duration_minutes, "priority": t.priority}
                for t in pet.get_tasks()
            ]
        )
    else:
        st.info(f"No tasks yet for {pet.name}. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generates today's schedule from the owner's pets and their tasks.")

if st.button("Generate schedule"):
    scheduler = Scheduler(date=str(date.today()))
    scheduler.generate(owner)
    st.text(scheduler.explain())
