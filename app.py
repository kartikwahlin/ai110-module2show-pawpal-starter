import streamlit as st
from pawpal_system import Task, Pet, Scheduler, Owner

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

st.subheader("Owner Setup")

if "owner" not in st.session_state:
    with st.form("owner_form"):
        owner_name = st.text_input("Owner name")
        day_start = st.number_input("Day start (24h)", min_value=0, max_value=23, value=8)
        day_end = st.number_input("Day end (24h)", min_value=0, max_value=23, value=22)
        submitted = st.form_submit_button("Create Owner")
        if submitted and owner_name:
            st.session_state.owner = Owner(owner_name, int(day_start), int(day_end))
            st.rerun()
else:
    owner = st.session_state.owner
    st.success(f"Owner: {owner.name} ({owner.day_start}:00 — {owner.day_end}:00)")

st.subheader("Pets")

if "owner" in st.session_state:
    owner = st.session_state.owner
    with st.form("pet_form"):
        pet_name = st.text_input("Pet name")
        submitted = st.form_submit_button("Add Pet")
        if submitted and pet_name:
            owner.add_pet(Pet(pet_name))
            st.rerun()
    if owner.pets:
        st.write("Current pets: " + ", ".join(p.name for p in owner.pets))
else:
    st.info("Create an owner first.")

st.subheader("Tasks")

if "owner" in st.session_state and st.session_state.owner.pets:
    owner = st.session_state.owner
    with st.form("task_form"):
        pet_choice = st.selectbox("Assign to pet", [p.name for p in owner.pets])
        task_name = st.text_input("Task name")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.number_input("Priority (lower = higher priority)", min_value=1, value=1)
        submitted = st.form_submit_button("Add Task")
        if submitted and task_name:
            pet = next(p for p in owner.pets if p.name == pet_choice)
            pet.tasks.append(Task(task_name, int(duration), int(priority)))
            st.rerun()

    for pet in owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}**")
            st.table([{"task": t.name, "duration": t.duration, "priority": t.priority} for t in pet.tasks])
else:
    st.info("Add an owner and at least one pet first.")

st.divider()

st.subheader("Build Schedule")

if "owner" in st.session_state and st.session_state.owner.pets:
    if st.button("Generate schedule"):
        scheduler = Scheduler(st.session_state.owner)
        schedule = scheduler.generate_times()
        if schedule:
            st.write("### Today's Schedule")
            for pet_name, task_name, start_minute in schedule:
                hours = start_minute // 60
                minutes = start_minute % 60
                st.write(f"`{hours:02d}:{minutes:02d}` — **{task_name}** ({pet_name})")
        else:
            st.info("No tasks to schedule.")
else:
    st.info("Add an owner, pets, and tasks to generate a schedule.")
