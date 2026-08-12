        # API Specification: Authenticate user

        ## Endpoint
        ```
        POST /api/v1/auth/login
        ```

        ## Description
        Accepts email+password, returns JWT with sub and role claims.

        ## Category
        `auth`

        ## Authentication
* **Required:** Yes
* **Type:** Bearer JWT
* **Header:** `Authorization: Bearer <token>`
* **Role Required:** Any authenticated user

        ## Sample Request Body
```json
{
    "email": "engineer@nexusai.dev",
    "password": "securePassword123"
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
        * See other `auth` category endpoints in this folder.

        ---
        *API Documentation — Nexus AI Innovations — Auto-generated v1 spec*
