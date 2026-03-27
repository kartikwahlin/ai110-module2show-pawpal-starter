# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**


3 core actions: Change profile data,
Add task, giving prio and duration. Name and description possible too
View plan
- Briefly describe your initial UML design.
    I made a profile, task, taskList and scheduler class.
    The first two are records. TaskList is a collectionf of Tasks.
    scheduler is a higher-level function that can generate visible schedules using profile information and tasks
- What classes did you include, and what responsibilities did you assign to each?
    I included the aforementioned classes. Most of the responsibility lies in the scheduler class. I wanted to keep things simple at the lower level, after claude mentioned that it was best to have modular, seperate classes. Initially, I wanted to have task as an internal structure in taskList, which would've made modification more difficult later.
**b. Design changes**

- Did your design change during implementation?
Yes.
- If yes, describe at least one change and why you made it.
I had to change from taskList to Pet. Renaming this class allowed me to have multiple pets tracked in one instance

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
It's most worried about time conflicts. Initially, my program would put all of the tasks in order from highest to lowest priority, but the section about time conflicts made me realize the user was supposed to input the start time for each task.
- How did you decide which constraints mattered most?
I looked at the assignment and tried to figure out what would match, and be practical in real life.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
It wants to use a helper function for two lambda sort functions
- Why is that tradeoff reasonable for this scenario?
It would help avoid repeating code, but at this scale, it's not that valuable.
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

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
