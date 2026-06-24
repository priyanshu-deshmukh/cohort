# Intern Capstone — 4-Day Build

## Cohort: the platform a learning program uses to run courses, not just host them

---

### The world you're building for

A training program runs courses the clumsy way. Materials live in a shared drive nobody can find. Assignments come in over email and get lost. Instructors grade in a spreadsheet and forget to tell students their marks. During live sessions, half the questions never get asked because there's no good way to raise a hand, and the ones that do get asked get forgotten. Students have no single place to see what they're enrolled in, what's due, and how they're doing.

You're building **Cohort** — the platform that runs a course end to end: enrolling students, handing out materials, collecting and grading work, running live sessions, and keeping every grade and submission in one place. Over the next four days you'll build a working product that a real student, a real instructor, and a real program admin could all sign into and use to get through a course.

This document describes **what the product does**. It does not tell you how to build it — that's the assignment. Read it as a product spec, decide what the thing needs to be, and build it.

---

### The three kinds of people who use Cohort

Everyone signs into their own account, and what they can see and do depends entirely on who they are. A person in one role should never be able to reach into another's world, even if they go looking.

**The Student** is there to learn. They can:
- Browse the catalogue and enrol in courses; see the courses they're enrolled in and nothing about courses they aren't.
- Open a course to find its materials and download them, see what's assigned, and read announcements.
- Submit their work by uploading their assignment files before the deadline.
- See their own grades and feedback — only their own — and track where they stand.
- Join live sessions and ask questions in them.
- Lean on the Study Coach (described below).

**The Instructor** teaches. They can:
- Manage *their own* courses — and only theirs. Post materials and announcements, create assignments with deadlines.
- See the students enrolled in their courses, who has submitted, and who hasn't.
- Open and grade submissions, leaving feedback that goes back to the student.
- Run live sessions and answer questions as they come in.

**The Program Admin** runs the whole program. They can:
- Create courses and assign instructors to them.
- Manage students and enrolments across everything.
- See the full picture — every course, every cohort's progress — that no single instructor sees.

These boundaries matter. A student who goes looking for another student's grades, or an instructor who tries to edit a course that isn't theirs, must be cleanly and clearly turned away — never shown data that isn't theirs, never left at a crash or a blank page.

---

### The journey through a course

This is the heart of the product. Follow one student through one course and you'll see most of what Cohort has to do.

It begins when a **student enrols**. The moment they do, they get a confirmation email welcoming them to the course, and the course appears in their list with its materials ready to download.

The **instructor posts an assignment** with a deadline. Every enrolled student is notified by email that there's new work, and it appears in their course. When a **student submits**, they upload their files; the submission form should be hard to get wrong, telling them clearly if they've attached the wrong thing or missed a required file rather than failing vaguely. Their submitted files become a permanent part of the record — long after the course ends, both student and instructor can pull up exactly what was handed in.

The **instructor grades the work**, leaving a mark and written feedback. The student is emailed that they've been graded and can read the feedback and see where they stand. Throughout, the instructor can see at a glance who has and hasn't submitted as a deadline approaches — and that view updates live as submissions land.

Running through the course are **live sessions**. When a session is on, students and the instructor are in it together: a student posts a question and it appears for the instructor and the other students **the instant it's asked**, with no refreshing; the instructor marks a question answered and everyone sees it resolve live. It feels like a room, not a page.

Every grade, every piece of feedback, and every submission stays on the record. A student can always see their full history in a course; an instructor and admin can always pull up exactly what was submitted and what was awarded.

---

### The Study Coach

Keeping on top of a course is hard, so Cohort gives each student an assistant they can talk to in plain language — the **Study Coach**. It's not a search box and it's not a bot that only talks; it actually *does things* on the student's behalf, and each student only ever sees their own, scoped to their own courses.

A student should be able to type a real request and have the Coach carry it out:

- **"What's due this week and how am I doing overall?"** — the Coach looks at their enrolments, deadlines, and grades, and tells them exactly where they stand.
- **"Submit these files for the assignment, and enrol me in the elective."** — the Coach actually makes the submission and the enrolment, the same way the student could by hand.
- **"Build me a study plan for the next two weeks based on what's coming up."** — the Coach produces a realistic plan from the student's actual deadlines and workload.

The Coach should be genuinely useful — a student should be able to stay organized and on track through conversation alone. When it takes an action, that action shows up everywhere else in the product exactly as if the student had done it.

---

### The session is alive

Cohort is not a page people refresh. A live session is a live room, and the submission view is a live picture of work coming in.

When a student asks a question in a session, the instructor and everyone else in the room sees it appear **on its own, the moment it's asked**. When the instructor marks it answered, it resolves on everyone's screen at once. As a deadline nears, the instructor watching the submission list sees each new submission land live, without touching anything.

If the product makes anyone hit refresh to see the latest question or submission, it isn't finished.

---

### How the product should behave when things go wrong

A good product stays calm and clear when things get messy. Cohort should:

- **Refuse what shouldn't be allowed, gracefully.** Reaching for another student's grades, or a course that isn't yours to teach, gets a clear, polite refusal — never someone else's data, never a crash.
- **Reject bad input helpfully.** Submission and course forms guard against nonsense and explain precisely what's wrong and how to fix it.
- **Explain the impossible.** When an action can't happen — submitting after a deadline has closed, enrolling in a course that's full — the person gets a precise, human explanation, not a generic error.
- **Keep accounts and sign-in trustworthy.** People sign in securely and stay signed in sensibly, and their credentials are protected.

The difference between a demo and a product is almost entirely in how it behaves on the bad path. Spend real attention here.

---

### What "done" looks like

By the end of day four, someone should be able to:

1. Sign up as a student, enrol in a course, and receive a confirmation email.
2. Have an instructor post an assignment that emails the cohort, then submit work by uploading files — with the form catching mistakes clearly.
3. Have the instructor grade that submission, emailing the student, and have the student read their feedback and see where they stand.
4. Run a live session where a question asked by a student appears instantly for the instructor and the room, and resolves live when answered.
5. Re-open the course later and still pull up exactly what was submitted and what was awarded.
6. Stay organized as a student through the Study Coach — asking what's due, having it submit work and enrol them, and getting a study plan from their real deadlines.

If all six work end to end, and the product stays clear-headed when someone misuses it, you've built Cohort.

---

### A suggested rhythm for the four days

This is guidance, not a rule — pace it however suits you.

- **Day 1** — Accounts and the three sign-in experiences; lock down the role boundaries early. Shape a course, an enrolment, and an assignment.
- **Day 2** — The full course journey end to end: enrol → materials → assignment → submit → grade → feedback. Get the data and the role rules right first.
- **Day 3** — Make the live session and the submission view real-time, and wire up the emails and the file uploads/records so everything persists exactly as submitted.
- **Day 4** — Build the Study Coach and its three abilities, then harden the bad paths — refusals, validation, clear failures — and polish.

Build something you'd be comfortable handing to a real instructor on the first day of a real course.
