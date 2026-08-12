        # API Specification: Get system configuration

        ## Endpoint
        ```
        GET /api/v1/system/config
        ```

        ## Description
        Returns non-sensitive system configuration. Admin-only.

        ## Category
        `system`

        ## Authentication
* **Required:** Yes
* **Type:** Bearer JWT
* **Header:** `Authorization: Bearer <token>`
* **Role Required:** `admin`


        ## Response Codes
        | Status Code       | Description                              |
        |-------------------|------------------------------------------|
        | 200 OK         | Successful operation                     |
        | 404 Not Found           | Resource error or validation failure     |
        | 401 Unauthorized  | Missing or invalid JWT token             |
        | 403 Forbidden     | Insufficient role permissions             |
        | 500 Internal Error| Unexpected server error                  |

        ## Rate Limiting
        * **Limit:** 200 req/min (authenticated)
        * **Headers:** `X-RateLimit-Remaining`, `X-RateLimit-Reset`

        ## Related Endpoints
        * See other `system` category endpoints in this folder.

        ---
        *API Documentation — Nexus AI Innovations — Auto-generated v1 spec*
