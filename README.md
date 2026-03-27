# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Features

- **Multi-pet management** — one owner can manage any number of pets, each with their own task list
- **Priority-based sorting** — tasks are ranked by priority so the most important care happens first
- **Time-based sorting** — tasks can be sorted chronologically by their user-set HH:MM time
- **Conflict detection** — the scheduler warns when two tasks for the same pet are scheduled at the same time
- **Recurring tasks** — daily and weekly tasks automatically reschedule themselves when marked complete, using Python's `timedelta`
- **Flexible filtering** — tasks can be filtered by completion status or by pet name
- **Streamlit UI** — owner, pet, and task data persists across reruns using `st.session_state`

<a href="/screen1.png" target="_blank"><img src='/screen1.png' title='PawPal App 1/2' width='' alt='PawPal App 1/2' class='center-block' /></a>
<a href="/screen2.png" target="_blank"><img src='/screen2.png' title='PawPal App 2/2' width='' alt='PawPal App 2/2' class='center-block' /></a>

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Smarter Scheduling
- Warns user about potential task conflicts
- Automatically refreshes daily and weekly tasks.

## Testing PawPal+
python -m pytest
My tests check to make sure that recurring tasks work properly, repeat conflicts are caught and flagged for the user, and sort/filter methods return properly modified lists of tasks.

Confidence level: 5
## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
