from datetime import date, time

import streamlit as st

from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.divider()

st.subheader("Owner")
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

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
    with col2:
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
    with col3:
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
    with col4:
        frequency = st.selectbox("Frequency", ["daily", "weekly", "one-time"], index=0)

    if st.button("Add task"):
        pet.add_task(
            Task(
                description=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
                date=str(date.today()),
            )
        )

    def render_task_rows(tasks):
        header = st.columns([3, 2, 2, 2, 2, 1])
        header[0].markdown("**Title**")
        header[1].markdown("**Duration**")
        header[2].markdown("**Priority**")
        header[3].markdown("**Frequency**")
        header[4].markdown("**Date**")
        header[5].markdown("**Done**")
        for t in tasks:
            row = st.columns([3, 2, 2, 2, 2, 1])
            row[0].write(t.description)
            row[1].write(f"{t.duration_minutes} min")
            row[2].write(t.priority)
            row[3].write(t.frequency)
            row[4].write(t.date or "—")
            marked_done = row[5].checkbox(
                "Done",
                value=t.completed,
                key=f"task_done_{id(t)}",
                label_visibility="collapsed",
            )
            if marked_done and not t.completed:
                t.mark_complete()
                st.rerun()
            elif not marked_done and t.completed:
                t.mark_incomplete()
                st.rerun()

    if pet.get_tasks():
        upcoming_tasks = [t for t in pet.get_tasks() if not t.completed]
        completed_tasks = [t for t in pet.get_tasks() if t.completed]

        st.write(f"**Upcoming for {pet.name}**")
        if upcoming_tasks:
            render_task_rows(upcoming_tasks)
        else:
            st.caption("Nothing upcoming.")

        st.write(f"**Completed for {pet.name}**")
        if completed_tasks:
            render_task_rows(completed_tasks)
        else:
            st.caption("Nothing completed yet.")

        st.caption("Checking a recurring (daily/weekly) task as done automatically adds its next occurrence.")
    else:
        st.info(f"No tasks yet for {pet.name}. Add one above.")

st.divider()

st.subheader("Build Schedule")
st.caption(
    "Generates today's schedule from the owner's pets and their tasks, "
    "using the Scheduler's priority-based algorithm."
)

if st.button("Generate schedule"):
    scheduler = Scheduler(date=str(date.today()))
    scheduler.generate(owner)
    st.session_state.scheduler = scheduler

scheduler = st.session_state.get("scheduler")

if scheduler is not None:
    schedule = scheduler.get_schedule()

    if schedule:
        st.success(
            f"✅ Scheduled {len(schedule)} task(s) using "
            f"{scheduler.total_minutes_used} of {owner.available_minutes} available minutes."
        )
        st.table(
            [
                {
                    "Time": f"{t.scheduled_time}–{t.end_time()}",
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                }
                for t in schedule
            ]
        )
    else:
        st.info("No tasks scheduled yet. Add pets and tasks above, then generate a schedule.")

    if scheduler.skipped_tasks:
        st.warning(
            f"⏭️ {len(scheduler.skipped_tasks)} task(s) didn't fit in the available time and were skipped:"
        )
        st.table(
            [
                {
                    "Pet": t.pet_name,
                    "Task": t.description,
                    "Duration (min)": t.duration_minutes,
                    "Priority": t.priority,
                }
                for t in scheduler.skipped_tasks
            ]
        )

    if scheduler.conflicts:
        st.error(
            f"🚨 {len(scheduler.conflicts)} scheduling conflict(s) detected — "
            "these tasks overlap in time:"
        )
        for task_a, task_b in scheduler.conflicts:
            st.markdown(
                f"- **{task_a.pet_name}: {task_a.description}** "
                f"({task_a.scheduled_time}–{task_a.end_time()}) overlaps with "
                f"**{task_b.pet_name}: {task_b.description}** "
                f"({task_b.scheduled_time}–{task_b.end_time()})"
            )
        st.caption(
            "Tip: reschedule one of the overlapping tasks, ask another person to cover one, "
            "or shorten a duration so they no longer collide."
        )

    with st.expander("Full text explanation"):
        st.text(scheduler.explain())
