        # API Specification: Get analytics dashboard data

        ## Endpoint
        ```
        GET /api/v1/admin/analytics
        ```

        ## Description
        Returns onboarding metrics, completion rates, and trends.

        ## Category
        `admin`

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
        * See other `admin` category endpoints in this folder.

        ---
        *API Documentation — Nexus AI Innovations — Auto-generated v1 spec*
