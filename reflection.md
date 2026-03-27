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
Ai was useful throughout the whole process, but I thought claude was most effective when I had to adjust my structure after finding out it was meant to be different in the assignment. It's quick at changing functions, and adjusting their usage in other parts of the code.
It was also powerful as a tool for generating documentation that would otherwise take a while to write.
- What kinds of prompts or questions were most helpful?
My strongest prompts involved me giving context, providing a suggestion, and asking for other ideas. Claude would then list out a variety of options, making it easy to determine the best one, and making sure I can trust the changes I then ask it to make.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
Claude wanted to refactor two functions to both rely on a helper. Since both functions were 1 line long anyways, due to using lambda, I thought it would just make the code harder to read.
- How did you evaluate or verify what the AI suggested?
I considered the output in both scenarios, and since it was a simple refactoring, I just needed to think about what would be easiest to read and potentially change.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
I tested sorting, conflict detection, and filtering behaviours.
- Why were these tests important?
Without these tests, I'd have to hand-construct different scenarios in the app to make sure these edge cases worked. With them, I don't have to spend so much time to know my code works

**b. Confidence**

- How confident are you that your scheduler works correctly?
5/5
- What edge cases would you test next if you had more time?
I think I would try testing much larger task lists, and ones involving overlapping daily tasks that don't conflict at the time of assignment.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I really liked creating the UML diagram, and coming up with a modular and scalable skeleton that was easy to change later on.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would probably want to make it easier to delete pets and tasks.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI is powerful, and has tons of programming experience, but needs guidance. It'll follow bad decisions, so you need to make sure your prompts point it in the right direction.