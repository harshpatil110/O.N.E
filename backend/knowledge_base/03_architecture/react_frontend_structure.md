# React Frontend Architecture

## Tech Stack
* **Framework:** React 18 with functional components and hooks.
* **Bundler:** Vite 5 (HMR, ESBuild-powered).
* **Styling:** Tailwind CSS 3.4 with custom design tokens.
* **Routing:** React Router v6.
* **State:** React Context API (AuthContext, ChecklistContext).
* **HTTP:** Axios for API communication.
* **Animations:** Framer Motion.

## Directory Structure
```
frontend/
├── src/
│   ├── api/
│   │   ├── auth.js          # login(), register()
│   │   ├── chat.js          # sendMessage(), getChatHistory()
│   │   └── admin.js         # getDevelopers(), getAnalytics()
│   ├── components/
│   │   ├── ChatUI.jsx       # Main chat interface
│   │   ├── MessageBubble.jsx
│   │   ├── ChatHistoryDrawer.jsx
│   │   └── Sidebar.jsx
│   ├── context/
│   │   ├── AuthContext.jsx   # AuthProvider (token + role)
│   │   └── ChecklistContext.jsx
│   ├── hooks/
│   │   ├── useAuth.js
│   │   └── useChat.js       # Chat message lifecycle
│   ├── pages/
│   │   ├── LoginPage.jsx
│   │   ├── DashboardPage.jsx
│   │   └── AdminDevelopersPage.jsx
│   ├── index.css            # Global styles + scrollbar overrides
│   └── main.jsx             # App entry point
├── index.html
├── vite.config.js
├── tailwind.config.js
└── package.json
```

## Key Patterns
* **Token Storage:** `sessionStorage` (not localStorage) for JWT.
* **Role-Based Routing:** Admin users redirect to `/admin`;
  employees go to `/dashboard`.
* **Optimistic Updates:** Chat messages appear immediately before
  server confirmation.

---
*Frontend Lead: Manas Gupta*
