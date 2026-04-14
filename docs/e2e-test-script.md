# O.N.E. End-to-End Test Script

Use this formatted script to manually walk through the application flow during a live demo or QA phase. Check the boxes as you successfully complete each step.

## Test Case 1: Happy Path — Senior Backend Python Developer

- [ ] **1.** Open `localhost:5173` and login as `dev@company.com`
- [ ] **2.** Observe that a new Session starts and the agent sends a welcome message.
- [ ] **3.** **Type:** "Hi, I'm Rahul Sharma, rahul@test.com"
- [ ] **4.** *Verify:* The agent extracts the name and email address into the system correctly.
- [ ] **5.** **Type:** "I'm a senior backend developer"
- [ ] **6.** *Verify:* Role is extracted and recognized as "backend".
- [ ] **7.** **Type:** "I mostly work with Python and FastAPI"
- [ ] **8.** *Verify:* The appropriate checklist is generated (you should see 10-12 matching tasks in the sidebar).
- [ ] **9.** **Type:** "What do I need to do for GitHub access?"
- [ ] **10.** *Verify:* The agent retrieves context from the knowledge base and cites its source accurately.
- [ ] **11.** **Type:** "I've set up GitHub access"
- [ ] **12.** *Verify:* The agent marks the checklist item as complete in the sidebar within ~3 seconds.
- [ ] **13.** Continue conversation naturally to complete at least 3 more items.
- [ ] **14.** *Verify:* The dashboard progress bar and status tags update properly.
- [ ] **15.** Finish all remaining required checklist items.
- [ ] **16.** **Type:** "I've finished everything"
- [ ] **17.** *Verify:* Agent recognizes completion and offers to send the HR notification email.
- [ ] **18.** **Type:** "Yes, please send it"
- [ ] **19.** *Verify:* You actually receive the properly formatted HTML notification in your Gmail inbox.

---

## Test Case 2: Alternate Path — Intern Frontend Developer

- [ ] **1.** Start a fresh session.
- [ ] **2.** Introduce yourself as a newly hired Junior/Intern Frontend Developer.
- [ ] **3.** *Verify:* The generated checklist is significantly different (e.g., it includes a basic "git workflow tutorial" and omits high-level system architecture / ADR review tasks).
- [ ] **4.** Ask a simple, entry-level question regarding the setup.
- [ ] **5.** *Verify:* Agent responses exhibit more "hand-holding", utilizing simpler terminology and more detailed steps based on your junior persona.

---

## Test Case 3: HR Admin Dashboard Verification

- [ ] **1.** Open a new tab to `localhost:5173` and login as your HR Admin (`patilha2005@gmail.com`).
- [ ] **2.** *Verify:* The `/dashboard` route loads successfully without redirecting you.
- [ ] **3.** *Verify:* Both the Senior Backend Developer and the Intern Frontend Developer sessions appear populated in the sessions table.
- [ ] **4.** *Verify:* The high-level KPI metrics cards (Completion Rate, Active Sessions) reflect accurate, up-to-date counts.
- [ ] **5.** Click "View" on the Senior Developer's session.
- [ ] **6.** *Verify:* The Session Details page accurately displays the employee details, and rendering matches the fully completed checklist exactly.
