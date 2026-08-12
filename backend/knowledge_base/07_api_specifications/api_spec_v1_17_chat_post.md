        # API Specification: Send chat message

        ## Endpoint
        ```
        POST /api/v1/chat/{session_id}/message
        ```

        ## Description
        Sends user message to Hermes Agent, returns AI response.

        ## Category
        `chat`

        ## Authentication
* **Required:** Yes
* **Type:** Bearer JWT
* **Header:** `Authorization: Bearer <token>`
* **Role Required:** Any authenticated user

        ## Sample Request Body
```json
{
    "message": "How do I set up my VPN?"
}
```

        ## Response Codes
        | Status Code       | Description                              |
        |-------------------|------------------------------------------|
        | 201 Created         | Successful operation                     |
        | 400 Bad Request           | Resource error or validation failure     |
        | 401 Unauthorized  | Missing or invalid JWT token             |
        | 403 Forbidden     | Insufficient role permissions             |
        | 500 Internal Error| Unexpected server error                  |

        ## Rate Limiting
        * **Limit:** 200 req/min (authenticated)
        * **Headers:** `X-RateLimit-Remaining`, `X-RateLimit-Reset`

        ## Related Endpoints
        * See other `chat` category endpoints in this folder.

        ---
        *API Documentation — Nexus AI Innovations — Auto-generated v1 spec*
