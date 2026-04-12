# API Contract

## Authentication

### 1. Login
- **Method & Path**: `POST /api/v1/auth/login`
- **Auth Requirement**: Public
- **Description**: Authenticate user and receive JWT.
- **Request**:
```json
{
  "email": "jane@example.com",
  "password": "securepassword123"
}
```
- **Response (200 OK)**:
```json
{
  "access_token": "eyJhbG...jwt.token",
  "token_type": "bearer"
}
```

### 2. Register Employee
- **Method & Path**: `POST /api/v1/auth/register-employee`
- **Auth Requirement**: JWT HR Admin
- **Description**: HR Admin registers a new employee.
- **Request**:
```json
{
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "employee"
}
```
- **Response (201 Created)**:
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Jane Doe",
  "email": "jane@example.com",
  "role": "employee",
  "created_at": "2026-04-12T10:00:00Z"
}
```

## Onboarding Sessions

### 3. Start Session
- **Method & Path**: `POST /api/v1/onboarding/start`
- **Auth Requirement**: JWT Employee
- **Description**: Initiate a new onboarding session.
- **Request**:
```json
{
  "user_id": "123e4567-e89b-12d3-a456-426614174000"
}
```
- **Response (201 Created)**:
```json
{
  "id": "session-uuid",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "status": "in_progress",
  "current_fsm_state": "WELCOME",
  "started_at": "2026-04-12T10:05:00Z"
}
```

### 4. Get Session Details
- **Method & Path**: `GET /api/v1/onboarding/{session_id}`
- **Auth Requirement**: JWT Employee or HR Admin
- **Description**: Retrieve session info and persona state.
- **Request**: Empty
- **Response (200 OK)**:
```json
{
  "id": "session-uuid",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "persona": {
    "name": "Jane",
    "role": "frontend"
  },
  "status": "in_progress",
  "current_fsm_state": "PROFILING",
  "started_at": "2026-04-12T10:05:00Z"
}
```

### 5. Get Session Progress
- **Method & Path**: `GET /api/v1/onboarding/{session_id}/progress`
- **Auth Requirement**: JWT Employee or HR Admin
- **Description**: Get checklist completion progress.
- **Request**: Empty
- **Response (200 OK)**:
```json
{
  "completed_items": 5,
  "total_items": 10,
  "percentage": 0.5
}
```

## Chat / Agent Communication

### 6. Send Chat Message
- **Method & Path**: `POST /api/v1/chat/{session_id}/message`
- **Auth Requirement**: JWT Employee
- **Description**: Send a message to the agent and receive response.
- **Request**:
```json
{
  "content": "Hello, I am ready to start my onboarding.",
  "metadata": {}
}
```
- **Response (200 OK)**:
```json
{
  "id": "msg-uuid",
  "session_id": "session-uuid",
  "role": "assistant",
  "content": "Welcome Jane! Let's get started...",
  "created_at": "2026-04-12T10:06:00Z"
}
```

### 7. Get Chat History
- **Method & Path**: `GET /api/v1/chat/{session_id}/history`
- **Auth Requirement**: JWT Employee or HR Admin
- **Description**: Fetch logs for rendering conversation history.
- **Request**: Empty
- **Response (200 OK)**:
```json
[
  {
    "id": "msg-uuid-user",
    "role": "user",
    "content": "Hi",
    "created_at": "2026-04-12T10:05:50Z"
  },
  {
    "id": "msg-uuid-assistant",
    "role": "assistant",
    "content": "Welcome!",
    "created_at": "2026-04-12T10:05:55Z"
  }
]
```

## Checklist Management

### 8. Update Checklist Item
- **Method & Path**: `PATCH /api/v1/checklist/{item_id}`
- **Auth Requirement**: JWT Employee (or Backend Agent)
- **Description**: Change status of an item.
- **Request**:
```json
{
  "status": "completed"
}
```
- **Response (200 OK)**:
```json
{
  "id": "item_id",
  "session_id": "session-uuid",
  "item_key": "github_access",
  "status": "completed",
  "completed_at": "2026-04-12T10:10:00Z"
}
```

### 9. Get Session Checklist
- **Method & Path**: `GET /api/v1/checklist/{session_id}`
- **Auth Requirement**: JWT Employee or HR Admin
- **Description**: Retrieve all checklist items for a session.
- **Request**: Empty
- **Response (200 OK)**:
```json
[
  {
    "id": "item_id",
    "item_key": "github_access",
    "title": "GitHub Access",
    "category": "access",
    "status": "completed"
  }
]
```

## Knowledge Base (RAG)

### 10. Ingest Document
- **Method & Path**: `POST /api/v1/knowledge/ingest`
- **Auth Requirement**: JWT HR Admin
- **Description**: Parse markdown/document and embed in ChromaDB.
- **Request**: (Multipart or JSON)
```json
{
  "content": "# Git Workflow...",
  "metadata": {"category": "engineering"}
}
```
- **Response (201 Created)**:
```json
{
  "message": "Successfully ingested chunks.",
  "chunks_added": 3
}
```

### 11. Query Knowledge Base
- **Method & Path**: `POST /api/v1/knowledge/query`
- **Auth Requirement**: JWT Employee or HR Admin
- **Description**: Test RAG retrieval directly (internal/debugging).
- **Request**:
```json
{
  "query": "How do I setup python?"
}
```
- **Response (200 OK)**:
```json
{
  "results": [
    {
      "content": "Setup python via pyenv...",
      "score": 0.89
    }
  ]
}
```

## Admin API

### 12. List Active Sessions
- **Method & Path**: `GET /api/v1/admin/sessions`
- **Auth Requirement**: JWT HR Admin
- **Description**: Overview of all onboarding statuses.
- **Request**: Empty
- **Response (200 OK)**:
```json
[
  {
    "id": "session-uuid",
    "user_email": "jane@example.com",
    "status": "in_progress",
    "progress": 50
  }
]
```

### 13. System Metrics
- **Method & Path**: `GET /api/v1/admin/metrics`
- **Auth Requirement**: JWT HR Admin
- **Description**: Retrieves high level statistics (completion rates).
- **Request**: Empty
- **Response (200 OK)**:
```json
{
  "total_employees_onboarded": 12,
  "average_completion_time_days": 2.5,
  "active_sessions": 3
}
```
