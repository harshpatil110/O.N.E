# O.N.E. End-to-End Test Script

Use this script to verify the complete onboarding flow from developer login to HR notification.

## Test Case 1: Happy Path — Senior Backend Python Developer

- [ ] **1.** Open browser and navigate to `localhost:5173`
- [ ] **2.** Login as `dev@company.com`
- [ ] **3.** Verify the session starts and the agent sends a greeting.
- [ ] **4.** **Type:** "Hi, I'm Rahul Sharma, rahul@test.com"
- [ ] **5.** **Verify:** Agent extracts name "Rahul Sharma" and email "rahul@test.com".
- [ ] **6.** **Type:** "I'm a senior backend developer"
- [ ] **7.** **Verify:** Role is recognized as "backend".
- [ ] **8.** **Type:** "I mostly work with Python and FastAPI"
- [ ] **9.** **Verify:** Checklist generated with 10-12 items relevant to Backend/Python.
- [ ] **10.** **Type:** "What do I need to do for GitHub access?"
- [ ] **11.** **Verify:** Agent retrieves info from knowledge base and cites a source.
- [ ] **12.** **Type:** "I've set up GitHub access"
- [ ] **13.** **Verify:** Sidebar checklist item for GitHub access marks as complete within 3 seconds.
- [ ] **14.** Continue through at least 3 more items (e.g., VPN, Local Dev Setup).
- [ ] **15.** **Verify:** Progress bar updates as items are completed.
- [ ] **16.** Complete all required checklist items.
- [ ] **17.** **Type:** "I've finished everything"
- [ ] **18.** **Verify:** Agent offers to send the HR completion email.
- [ ] **19.** **Type:** "Yes, please send it"
- [ ] **20.** **Verify:** HR email received in Gmail (check `HR_EMAIL`).

---

## Test Case 2: Alternate Path — Intern Frontend Developer

- [ ] **1.** Start a new session or login as a new user.
- [ ] **2.** Identify as "Intern Frontend Developer".
- [ ] **3.** **Verify:** Checklist contains "git workflow tutorial" and excludes "ADR review".
- [ ] **4.** **Verify:** Agent response style is more supportive/detailed for an intern persona.

---

## Test Case 3: HR Admin Dashboard

- [ ] **1.** Login as `patilha2005@gmail.com` (or current HR Admin user).
- [ ] **2.** **Verify:** Both the Senior Backend and Intern Frontend developer sessions are visible in the table.
- [ ] **3.** **Verify:** Dashboard metrics (Total Sessions, Avg Completion, etc.) are calculated correctly.
- [ ] **4.** **Click:** "View" on a session.
- [ ] **5.** **Verify:** Session detail view shows the correct checklist state and employee metrics.
