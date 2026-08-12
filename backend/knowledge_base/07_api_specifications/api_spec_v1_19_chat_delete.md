        # API Specification: Clear chat history

        ## Endpoint
        ```
        DELETE /api/v1/chat/{session_id}
        ```

        ## Description
        Deletes all messages in a chat session. Admin-only.

        ## Category
        `chat`

        ## Authentication
* **Required:** Yes
* **Type:** Bearer JWT
* **Header:** `Authorization: Bearer <token>`
* **Role Required:** Any authenticated user


        ## Response Codes
        | Status Code       | Description                              |
        |-------------------|------------------------------------------|
        | 204 No Content         | Successful operation                     |
        | 404 Not Found           | Resource error or validation failure     |
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
