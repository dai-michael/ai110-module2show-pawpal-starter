# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

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

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
Today's Schedule
Plan for 2026-07-03:
  08:00-08:30 — Mochi: Morning walk (30 min) [priority: high]
  08:30-08:40 — Mochi: Feeding (10 min) [priority: high]
  08:40-08:45 — Biscuit: Litter box cleaning (5 min) [priority: medium]
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python -m pytest
```

`tests/test_pawpal.py` covers the three scheduling behaviors most likely to break: sorting correctness of  `get_schedule()`, completing a recurring task creates the next task, and scheduler flags duplicate times with `find_conflicts()` 

Sample test output:

```
======================================================================= test session starts =======================================================================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/weidai/codepath/ai110/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 10 items                                                                                                                                                

tests/test_pawpal.py ............                                                                                                                           [100%]

======================================================================= 10 passed in 0.01s ========================================================================
```

4/5 star confidence reliability

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.generate()` | Greedily packs tasks by priority tier (high → medium → low), back-to-back from the preferred start time. |
| Filtering | `Scheduler.generate()`, `Owner.filter_tasks()` | Skips tasks that don't fit remaining time; `filter_tasks()` narrows by pet name and/or completion status. |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler._times_overlap()` | Flags overlapping scheduled times across all pets; surfaced as a warning in `explain()` |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()` | Completing a "daily"/"weekly" task automatically creates the next unscheduled occurrence. |

## 📸 Demo Walkthrough

The Streamlit UI (`app.py`) lets a user:

- Enter owner info (name, available minutes, preferred start time, priority preference)
- Add one or more pets (name, species, age, breed)
- Add tasks to a selected pet (title, duration, priority)
- Generate a schedule and view scheduled tasks, skipped tasks, and time conflicts
- Read a full text explanation of the plan

**Example workflow:** add a pet ("Mochi") → add a task ("Morning walk", 30 min, high priority) → click **Generate schedule** → view today's schedule, sorted by start time.

**Key scheduler behaviors shown in the UI:**

1. **Sorting** — scheduled tasks are shown in time order regardless of the order they were entered in.
2. **Priority-first packing** — high-priority tasks are scheduled before lower-priority ones when time is limited.
3. **Skipped tasks** — tasks that don't fit in the owner's available minutes are listed separately with a warning.
4. **Conflict warnings** — overlapping scheduled times across different pets are flagged in red with a suggested fix.

Sample CLI output (`python main.py`), showing sorting, priority packing, filtering, and conflict detection:

```
Today's Schedule
Plan for 2026-07-03:
  08:00-08:10 — Mochi: Feeding (10 min) [priority: high]
  08:10-08:40 — Mochi: Morning walk (30 min) [priority: high]
  08:40-09:00 — Biscuit: Vet checkup (20 min) [priority: high]
  09:00-09:10 — Mochi: Brushing (10 min) [priority: medium]
  09:10-09:15 — Biscuit: Litter box cleaning (5 min) [priority: medium]

Scheduled tasks sorted by time:
  08:00 — Mochi: Feeding
  08:10 — Mochi: Morning walk
  08:40 — Biscuit: Vet checkup
  09:00 — Mochi: Brushing
  09:10 — Biscuit: Litter box cleaning

Incomplete tasks (filtered):
  Mochi: Feeding [high]
  Mochi: Morning walk [high]
  Mochi: Brushing [medium]
  Biscuit: Vet checkup [high]
  Biscuit: Litter box cleaning [medium]

Completed tasks (filtered):
  Mochi: Nail trim [low]

Tasks for Mochi only (filtered):
  Feeding [high]
  Nail trim [low]
  Morning walk [high]
  Brushing [medium]

Today's Schedule (with a scheduling conflict introduced)
Plan for 2026-07-03:
  08:00-08:10 — Mochi: Feeding (10 min) [priority: high]
  08:10-08:40 — Mochi: Morning walk (30 min) [priority: high]
  08:40-09:00 — Biscuit: Vet checkup (20 min) [priority: high]
  09:00-09:10 — Mochi: Brushing (10 min) [priority: medium]
  09:10-09:15 — Biscuit: Litter box cleaning (5 min) [priority: medium]
  10:00-10:30 — Mochi: Grooming appointment (30 min) [priority: medium]
  10:10-10:25 — Biscuit: Vet follow-up call (15 min) [priority: high]
Conflicts (overlapping times):
  - Mochi: Grooming appointment (10:00-10:30) overlaps Biscuit: Vet follow-up call (10:10-10:25)
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
