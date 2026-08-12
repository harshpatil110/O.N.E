# REST API Design Conventions — Nexus AI Innovations

## URL Structure
All endpoints follow the pattern:
```
/api/v1/<resource>/<action>
```

## HTTP Methods
| Method | Usage                          | Example                        |
|--------|--------------------------------|--------------------------------|
| GET    | Retrieve resource(s)           | `GET /api/v1/users`            |
| POST   | Create a resource              | `POST /api/v1/auth/login`      |
| PUT    | Full update of a resource      | `PUT /api/v1/users/{id}`       |
| PATCH  | Partial update                 | `PATCH /api/v1/sessions/{id}`  |
| DELETE | Remove a resource              | `DELETE /api/v1/users/{id}`    |

## Response Format
All responses use a consistent JSON envelope:
```json
{
    "data": { ... },
    "meta": {
        "request_id": "uuid-v4",
        "timestamp": "ISO-8601"
    }
}
```

## Error Responses
```json
{
    "detail": "Invalid email or password",
    "status_code": 401
}
```

## Authentication
* All protected endpoints require a Bearer JWT token in the
  `Authorization` header.
* Admin endpoints require `role == "admin"` in the JWT claims.

## Pagination
Use query parameters for paginated endpoints:
```
GET /api/v1/admin/developers?page=1&limit=20
```

## Rate Limiting
* Public endpoints: 60 requests/minute per IP.
* Authenticated endpoints: 200 requests/minute per user.
* Rate limit headers: `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

---
*API Standards: Archit Verma*
