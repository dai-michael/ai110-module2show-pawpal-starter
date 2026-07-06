# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Three core actions a user should perform:
Add a pet and see pet needs
Input constraints for pet care
Automatically produce a plan 

My design uses a Scheduler class to act as the "brain" that retrieves, organizes, and manages tasks across pets, pulling from an Owner that can manage multiple pets at once.

Included classes:
Task:
    Responsibilities:
        Represents a single activity (description, time, frequency, completion status).
Pet:
    Responsibilities:
        Stores pet details and a list of tasks.
Owner:
    Responsibilities:
        Manages multiple pets and provides access to all their tasks.
Scheduler:
    Responsibilities:
        The "brain" that retrieves, organizes, and manages tasks across pets.


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.
Design changed during implementation. One change I made was the scheduler now has conflict detection. I made this change so the scheduler can detect and notify the user if certain tasks have conflicting times, as previously my design did not consider this. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
My scheduler considered time and priority, along with preferences such as available minutes and preferred start time. I decided which constraints mattered most by first looking at what could not have any compromises, which I decided were available minutes and preferred start time. Then I looked at which tasks were most important, and prioritized fitting in high priority tasks over low priority tasks.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff my scheduler makes is that it schedules tasks greedily by priority instead of solving for the combination of tasks that best fills the available time (like a knapsack approach would). My scheduler sorts all tasks by priority tier and packs them in that order until time runs out, so a single high-priority task has priority over several smaller lower-priority tasks.
I think this is reasonable, as though cost is that leftover time between tasks isn't used as efficiently as it could be, it makes the tasks easier to explain and also the code and logic is easier for humans to read. 

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used AI tools for design brainstorming, debugging, refactoring, generating an initial draft of features, creating the uml diagrams, and asking algorithmic questions. Prompts and questions I found most helpful were prompts that asked to explain the codebase or a specific bug that occured. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I asked AI to create a mermaid diagram using my high level description of my classes and it gave me an extra class called CareNeed. The logic behind the class made sense, however for some reason it was dependent on Task, so I pushed back on the suggestion and the AI reversed it's decision. I evaluated what the AI suggested by thinking through the intended flow of the program and double checking with the AI generated diagram.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I tested the following behaviors: sorting (`get_schedule()` returns tasks in chronological order and puts unscheduled tasks first), recurrence (completing a daily/weekly task spawns a correctly-dated next occurrence, while a non-recurring or unattached task does not), and conflict detection (`find_conflicts()` flags identical and partially overlapping times but not back-to-back tasks, and `generate()`'s own packing never produces a self-inflicted conflict). These mattered most because they're the parts of the scheduler that are easy to get subtly wrong (off-by-one overlap checks, forgetting to skip completed tasks) and hard to notice by just looking at a demo run.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I would put my confidence around 4/5 since I confirmed the core packing, sorting, and conflict logic with automatic tests and by manually running `main.py` and the Streamlit app. I'm less confident about edge cases with different combinations of priorities, minutes, owners, pets, and completed and uncompleted tasks. With more time I would create more tests for these edge cases that I'm less confident about. 

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
The part of the project I am most satisfied about is the upcoming and completed tasks lists because I think the design is intuitive and also extends the original idea I had for the app.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
If I had another iteration, I would redesign the tasks feature to allow users to schedule tasks for different weekdays

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
One important thing I learned about designing systems was that UML diagrams are a great way for us to manage what the AI is doing at a high level, and also very useful for communicating to the AI exactly what we want built. 
