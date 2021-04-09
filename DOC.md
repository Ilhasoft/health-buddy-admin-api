# HealthBuddy Admin Api

## Endpoints

- ## Authentication

    - ### **/token/ - `POST`**

        Generates authentication token from username and password, this token is required for every other request. This token has an 1 hour duration.

        - Request Body:
            ```json
            {
                "username": "admin",
                "password": "password123"
            }
            ```
        
        - Response body:
            ```json
            {
                "refresh": "<refresh_token>",
                "access": "<access_token>"
            }
            ```
            ` Status: 200 `

    - ### **/token/refresh/ - `POST`**

        Refresh the obtained access token on `/token/` for +1 hour of usage

        - Request body:
            ```json
            {
                "refresh": "<refresh_token>"
            }
            ``` 

        - Response body:
            ```json
            {
                "access": "<access_token>"
            }
            ``` 
            ` Status: 200 `

- ## Users

    - ### **/api/users - `GET`**

        List all users.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "count": 2,
                "next": "http://localhost:8000/api/users?page=2",
                "previous": null,
                "results": [
                    {
                        "url": "http://localhost:8000/api/users/1",
                        "id": 21,
                        "username": "admin",
                        "email": "admin@admin.com",
                        "first_name": "Admin",
                        "last_name": "Super",
                        "is_staff": true,
                        "is_active": true
                    },
                    {
                        "url": "http://localhost:8000/api/users/2",
                        "id": 2,
                        "username": "User",
                        "email": "user@user.com",
                        "first_name": "User",
                        "last_name": "NotSuper",
                        "is_staff": false,
                        "is_active": true
                    },
                ]
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id} - `GET`**

        List a single user information from the user id.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "url": "http://localhost:8000/api/users/2",
                "id": 2,
                "username": "User",
                "email": "user@user.com",
                "first_name": "User",
                "last_name": "NotSuper",
                "is_staff": false,
                "is_active": true
            },
            ```
            ` Status: 200 `

    - ### **/api/users/my_profile - `GET`**

        Get the user profile from the authentication token provided linked to that user.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "url": "http://localhost:8000/api/users/1",
                "id": 1,
                "username": "admin",
                "email": "admin@admin.com",
                "first_name": "Admin",
                "last_name": "Super",
                "is_staff": true,
                "is_active": true
            },
            ```
            ` Status: 200 `

     - ### **/api/users - `POST`**

        Creates a new user.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Request body:
            ```json
            {
                "username": "johnsmith",
                "password": "password123",
                "email": "john@mail.com",
                "first_name": "John",
                "last_name": "Smith"
            }
            ``` 
            ` Status: 201 `

        - Response Body:
            ```json
            {
                "url": "http://localhost:8000/api/users/3",
                "id": 3,
                "username": "johnsmith",
                "email": "johnsmith@main.com",
                "first_name": "John",
                "last_name": "Smith",
                "is_staff": false,
                "is_active": true
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id} - `PUT`**

        Updates an existing user information from id

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Request body:
            ```json
            {
                "username": "smithjohn",
                "password": "password123",
                "email": "john@mail.com",
                "first_name": "John",
                "last_name": "Smith"
            }
            ``` 

        - Response Body:
            ```json
            {
                "url": "http://localhost:8000/api/users/3",
                "id": 3,
                "username": "smithjohn",
                "email": "johnsmith@main.com",
                "first_name": "John",
                "last_name": "Smith",
                "is_staff": false,
                "is_active": true
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id} - `PATCH`**

        Updates defined fields from an existing user based on id.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Request body:
            ```json
            {
                "email": "mail@john.com",
                "first_name": "Johnnny",
                "last_name": "Smitherson"
            }
            ``` 

        - Response Body:
            ```json
            {
                "url": "http://localhost:8000/api/users/3",
                "id": 3,
                "username": "smithjohn",
                "email": "mail@john.com",
                "first_name": "Johnnny",
                "last_name": "Smitherson",
                "is_staff": false,
                "is_active": true
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id}/change_password - `PUT`**

        Updates user password, the `access_token` must be the users's one.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Request body:
            ```json
            {
                "current_password": "password123",
                "new_password": "123password"
            }
            ``` 

        - Response Body:
            ```json
            {
                "message": "smithjohn password was changed"
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id}/change_permission - `PUT`**

        Updates user permission type.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "message": "smithjohn permission has been changed"
            }
            ```
            ` Status: 200 `

    - ### **/api/users/{id} - `DEL`**

        Deactivates user.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:

            ` Status: 204 `

    - ### **/api/users/{id}/active_user - `PATCH`**

        Reactivate user.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "message": "smithjohn user has been activated!"
            }
            ```
            ` Status: 200 `

- ## Flows

    - ### **/api/flows - `GET`**

        Lists all registered flows.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "count": 2,
                "next": "http://localhost:8000/api/flows?page=2",
                "previous": null,
                "results": [
                    {
                        "uuid": "8715f9df-858a-49de-878b-a431f0b42ce5",
                        "name": "Flow1",
                        "is_active": true
                    },
                    {
                        "uuid": "87157632-132c-4e68-a26a-0b42ce541682",
                        "name": "Flow2",
                        "is_active": true
                    },
                ]
            }
            ```
            ` Status: 200 `

    - ### **/api/flows - `POST`**

        Register a new flow to be used in data collection.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Request body:
            ```json
            {
                "uuid": "8715f9df-858a-49de-a26a-0b42ce541682",
                "name": "test-flow"
            }
            ``` 

        - Response Body:
            ```json
            {
                "uuid": "8715f9df-858a-49de-a26a-0b42ce541682",
                "name": "test-flow",
                "is_active": true
            }
            ```
            ` Status: 201 `

- ## Daily Counters

    - ### **/rapidpro/labels_count - `GET`**

        Retrieves the daily counters for all labels in a specific query for one is not provided, in a date range.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters (all optional):
            ```yaml
            {
                uuid: "f5b6ad36-6ec7-4bf1-913c-a3484e7c5b3f",
                start_date: 2021-03-03,
                end_date: 2021-03-04
            }
            ``` 

        - Response Body:
            ```json
            [
                {
                    "uuid": "f5b6ad36-6ec7-4bf1-913c-a3484e7c5b3f",
                    "name": "test-label",
                    "msg_count": 4742
                },
            ]
            ```
            ` Status: 200 `

    - ### **/rapidpro/runs/most_accessed/completed - `GET`**

        Retrieves the completed flow execution counters for all flows, in a date range.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters (all optional):
            ```yaml
            {
                start_date: 2021-03-03,
                end_date: 2021-03-04
            }
            ``` 

        - Response Body:
            ```json
            [
                {
                    "uuid": "8715f9df-858a-49de-878b-a431f0b42ce5",
                    "name": "Flow1",
                    "active": 0,
                    "completed": 5053,
                    "interrupted": 0,
                    "expired": 0
                },
                {
                    "uuid": "87157632-132c-4e68-a26a-0b42ce541682",
                    "name": "Flow2",
                    "active": 79,
                    "completed": 4712,
                    "interrupted": 44,
                    "expired": 0
                },
            ]
            ```
            ` Status: 200 `

- ## Dashboard

    - ### **/rapidpro/runs/ - `GET`**

        Retrives the total counter of flow runs for all registered flows or a specified one, in a date range.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters (all optional):
            ```yaml
            {
                flow: "8715f9df-858a-49de-a26a-0b42ce541682",
                start_date: 2021-03-03,
                end_date: 2021-03-04
            }
            ``` 

        - Response Body:
            ```json
            {
                "completed": 226166,
                "interrupted": 1,
                "expired": 0,
                "active": 0
            }
            ```
            ` Status: 200 `

    - ### **/rapidpro/runs/all/ - `GET`**

        Retrives the daily counter of a specific flow, in a date range.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters:
            ```yaml
            {
                flow__uuid: "8715f9df-858a-49de-a26a-0b42ce541682", // MANDATORY
                start_date: 2021-03-03, // OPTIONAL
                end_date: 2021-03-04, // OPTIONAL
            }
            ``` 

        - Response Body:
            ```json
            [
                {
                    "flow": {
                        "uuid": "8715f9df-858a-49de-a26a-0b42ce541682",
                        "name": "Interaction counter",
                        "is_active": false
                    },
                    "active": 0,
                    "completed": 4,
                    "interrupted": 1,
                    "expired": 0,
                    "day": "2020-03-03T00:00:00Z"
                },
                {
                    "flow": {
                        "uuid": "8715f9df-858a-49de-a26a-0b42ce541682",
                        "name": "Interaction counter",
                        "is_active": false
                    },
                    "active": 0,
                    "completed": 3,
                    "interrupted": 0,
                    "expired": 0,
                    "day": "2020-03-04T00:00:00Z"
                },
            ]
            ```
            ` Status: 200 `

    - ### **/rapidpro/proxy/groups - `GET`**

        Retrives a list of all the RapidPro groups with their counts, in a date range.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters (all optional):
            ```yaml
            {
                start_date: 2021-03-03,
                end_date: 2021-03-04
            }
            ``` 

        - Response Body:
            ```json
            {
                "next": null,
                "previous": null,
                "results": [
                    {
                        "uuid": "77d1ff7bb-4b8c-4f5d-94c6-ff7bbad5667",
                        "name": "Language = Serbian",
                        "query": "language = \"srp\"",
                        "status": "ready",
                        "count": 13
                    },
                    {
                        "uuid": "1b6ed45e-be99-4913-9fbd-d45e4a61b6e",
                        "name": "Language = Albanian",
                        "query": "language = \"alb\"",
                        "status": "ready",
                        "count": 2
                    },
                ]
            }
            ```
            ` Status: 200 `

    - ### **/rapidpro/proxy/labels - `GET`**

        Retrives a list of all the RapidPro labels with their counts, or just a specified one.
        Note that this endpoint can not be filtered by date, for that use `/rapidpro/labels_count`

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

         - Query parameters (all optional):
            ```yaml
            {
                uuid: "f5b6ad36-6ec7-4bf1-913c-a3484e7c5b3f"
            }
            ``` 

        - Response Body:
            ```json
            {
                "next": null,
                "previous": null,
                "results": [
                    {
                        "uuid": "21e838cc-2028-49d0-8c43-f479d2979edb",
                        "name": "Low confidence response - French",
                        "count": 13
                    },
                    {
                        "uuid": "c6f6c896-152c-42af-baf7-34c2316093ba",
                        "name": "Low confidence response - Polish",
                        "count": 65
                    }
                ],
            }
            ```
            ` Status: 200 `

    - ### **/rapidpro/proxy/channel_stats - `GET`**

        Retrives a list of channels, and their respective stats.

        - Request Header:
            ```json
            {
                "Authorization": "Bearer <access_token>"
            }
            ```

        - Response Body:
            ```json
            {
                "count": 1,
                "next": null,
                "previous": null,
                "results": [
                    {
                        "uuid": "fffd645f-87fb-4417-b34a-fffd645d164f",
                        "name": "Channel1",
                        "channel_type": "EX",
                        "msg_count": 40,
                        "ivr_count": 0,
                        "error_count": 0,
                        "daily_counts": [
                            {
                                "name": "Incoming",
                                "type": "msg",
                                "data": [
                                    {
                                        "date": "2021-01-07",
                                        "count": 6
                                    },
                                    {
                                        "date": "2021-01-11",
                                        "count": 12
                                    },
                                ]
                            },
                            {
                                "name": "Outgoing",
                                "type": "msg",
                                "data": [
                                    {
                                        "date": "2021-01-07",
                                        "count": 3
                                    },
                                    {
                                        "date": "2021-01-11",
                                        "count": 19
                                    },
                                ]
                            },
                            {
                                "name": "Errors",
                                "type": "error",
                                "data": []
                            },
                        ],
                        "monthly_totals": [
                            {
                                "month_start": "2021-04-01T00:00:00Z",
                                "incoming_messages_count": 18,
                                "outgoing_messages_count": 22,
                                "incoming_ivr_count": 0,
                                "outgoing_ivr_count": 0,
                                "error_count": 0
                            },
                        ]
                    },
                ]
            }
            ```
            ` Status: 200 `