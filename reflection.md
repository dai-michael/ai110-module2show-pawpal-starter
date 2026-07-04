# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?
Three core actions a user should perform:
Add a pet and see pet needs
Input constraints for pet care
Automatically produce a plan 

My initial UML design uses one class, Plan, to ultimately generate and store a plan. It combines information from classes like PetInfo and OwnerInfo to generate tasks. 

Included classes:
Pet info: 
    Responsibilities:
        High level class that stores all pet information, and pet care information in a CareNeed class. Manages changes to care needs.
Owner info:
    Responsibilities:
        Stores all information relating to the owner (time available, priority, owner preferences)
Plan:
    Responsibilites:
        Uses pet info and owner information to create and store a schedule consisting of multiple owned task classes 
Task:
    Responsibilities:
        Stores information relating to a task. Namely, 
CareNeed:
    Responsibilities:
        Stores information about a need: what it is, frequency, priority, duration


**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
I asked AI to create a mermaid diagram using my high level description of my classes and it gave me an extra class called CareNeed. The logic behind the class made sense, however for some reason it was dependent on Task, so I pushed back on the suggestion and the AI reversed it's decision. I evaluated what the AI suggested by thinking through the intended flow of the program and double checking with the AI generated diagram.
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
