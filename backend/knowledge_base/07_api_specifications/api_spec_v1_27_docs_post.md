        # API Specification: Ingest new document

        ## Endpoint
        ```
        POST /api/v1/docs/ingest
        ```

        ## Description
        Uploads and indexes a new markdown document into ChromaDB.

        ## Category
        `docs`

        ## Authentication
* **Required:** Yes
* **Type:** Bearer JWT
* **Header:** `Authorization: Bearer <token>`
* **Role Required:** Any authenticated user

        ## Sample Request Body
```json
{
    "data": "See schema definition for field details."
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
        * See other `docs` category endpoints in this folder.

        ---
        *API Documentation — Nexus AI Innovations — Auto-generated v1 spec*
