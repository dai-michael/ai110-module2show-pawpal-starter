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

`tests/test_pawpal.py` covers the three scheduling behaviors most likely to break silently: that `get_schedule()` always returns tasks in chronological order (including unscheduled tasks), that completing a recurring task correctly rolls its date forward (one day for "daily", seven for "weekly") and spawns the next occurrence, and that `find_conflicts()` flags overlapping and duplicate-time tasks while correctly *not* flagging back-to-back tasks that just touch at the boundary.

Sample test output:

```
======================================================================= test session starts =======================================================================
platform darwin -- Python 3.14.2, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/weidai/codepath/ai110/ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 12 items                                                                                                                                                

tests/test_pawpal.py ............                                                                                                                           [100%]

======================================================================= 12 passed in 0.01s ========================================================================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.generate()` | Greedily packs tasks by priority tier (high → medium → low), back-to-back from the preferred start time. |
| Filtering | `Scheduler.generate()`, `Owner.filter_tasks()` | Skips tasks that don't fit remaining time; `filter_tasks()` narrows by pet name and/or completion status. |
| Conflict handling | `Scheduler.find_conflicts()`, `Scheduler._times_overlap()` | Flags overlapping scheduled times across all pets; surfaced as a warning in `explain()` |
| Recurring tasks | `Task.next_occurrence()`, `Task.mark_complete()` | Completing a "daily"/"weekly" task autotomatically creates the next unscheduled occurrence. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
