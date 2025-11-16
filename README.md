# On Way Study API

This is the backend API for the On Way Study application. It provides services for a frontend application that allows users to register and organize their progress in a university academic course. The user can register courses, subjects, activities, their grades, due dates, etc.

## Setup

To run this project, you will need to have Docker and Docker Compose installed on your machine.

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd on-way-study-api
    ```

2.  **Create a `.env` file:**
    Create a `.env` file in the root of the project and add the following environment variables:
    ```
    ON_WAY_STUDY_API_KEY_SIGNARURE=<your_api_key_signature>
    ```

3.  **Build and run the Docker containers:**
    ```bash
    docker-compose up --build
    ```

The API will be running at `http://localhost:8000`.

## Usage

Once the containers are running, you can access the API endpoints.

## API Documentation

### Authentication

All requests to the API must include the `X-On-Way-Study-Api-Signature` header with the value of your API key signature.

### Endpoints

#### Users

*   **`POST /api/users/`**: Create a new user.
    *   **Request Body**:
        ```json
        {
            "nickname": "string",
            "password": "string"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "nickname": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "institutions": []
        }
        ```
*   **`GET /api/users/{id}/`**: Retrieve a user.
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "nickname": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "institutions": [
                {
                    "id": "integer",
                    "name": "string",
                    "created_at": "datetime",
                    "updated_at": "datetime",
                    "courses": []
                }
            ]
        }
        ```
*   **`PUT /api/users/{id}/`**: Update a user.
    *   **Request Body**:
        ```json
        {
            "nickname": "string",
            "password": "string"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "nickname": "string",
            "created_at": "datetime",
            "updated_at": "datetime",
            "institutions": []
        }
        ```
*   **`DELETE /api/users/{id}/`**: Delete a user.

#### Institutions

*   **`POST /api/institutions/`**: Create a new institution.
    *   **Request Body**:
        ```json
        {
            "name": "string"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "user": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`GET /api/institutions/`**: Get a list of institutions.
    *   **Response Body**:
        ```json
        [
            {
                "id": "integer",
                "name": "string",
                "user": "integer",
                "created_at": "datetime",
                "updated_at": "datetime"
            }
        ]
        ```
*   **`GET /api/institutions/{id}/`**: Retrieve an institution.
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "user": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`PUT /api/institutions/{id}/`**: Update an institution.
    *   **Request Body**:
        ```json
        {
            "name": "string"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "user": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`DELETE /api/institutions/{id}/`**: Delete an institution.

#### Courses

*   **`POST /api/courses/`**: Create a new course.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "acronym": "string",
            "semesters": "integer",
            "institution": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "acronym": "string",
            "semesters": "integer",
            "institution": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`GET /api/courses/`**: Get a list of courses.
    *   **Response Body**:
        ```json
        [
            {
                "id": "integer",
                "name": "string",
                "acronym": "string",
                "semesters": "integer",
                "institution": "integer",
                "created_at": "datetime",
                "updated_at": "datetime"
            }
        ]
        ```
*   **`GET /api/courses/{id}/`**: Retrieve a course.
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "acronym": "string",
            "semesters": "integer",
            "institution": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`PUT /api/courses/{id}/`**: Update a course.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "acronym": "string",
            "semesters": "integer",
            "institution": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "acronym": "string",
            "semesters": "integer",
            "institution": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`DELETE /api/courses/{id}/`**: Delete a course.

#### Disciplines

*   **`POST /api/disciplines/`**: Create a new discipline.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "extra_information": "string",
            "semester": "integer",
            "final_grade": "decimal",
            "final_result": "string",
            "course": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "extra_information": "string",
            "semester": "integer",
            "final_grade": "decimal",
            "final_result": "string",
            "course": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`GET /api/disciplines/`**: Get a list of disciplines.
    *   **Response Body**:
        ```json
        [
            {
                "id": "integer",
                "name": "string",
                "extra_information": "string",
                "semester": "integer",
                "final_grade": "decimal",
                "final_result": "string",
                "course": "integer",
                "created_at": "datetime",
                "updated_at": "datetime"
            }
        ]
        ```
*   **`GET /api/disciplines/{id}/`**: Retrieve a discipline.
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "extra_information": "string",
            "semester": "integer",
            "final_grade": "decimal",
            "final_result": "string",
            "course": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`PUT /api/disciplines/{id}/`**: Update a discipline.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "extra_information": "string",
            "semester": "integer",
            "final_grade": "decimal",
            "final_result": "string",
            "course": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "extra_information": "string",
            "semester": "integer",
            "final_grade": "decimal",
            "final_result": "string",
            "course": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`DELETE /api/disciplines/{id}/`**: Delete a discipline.

#### Activities

*   **`POST /api/activities/`**: Create a new activity.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "status": "string",
            "grade_weight": "decimal",
            "expected_grade": "decimal",
            "grade_result": "decimal",
            "delivery_date": "datetime",
            "discipline": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "status": "string",
            "grade_weight": "decimal",
            "expected_grade": "decimal",
            "grade_result": "decimal",
            "delivery_date": "datetime",
            "discipline": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`GET /api/activities/`**: Get a list of activities.
    *   **Response Body**:
        ```json
        [
            {
                "id": "integer",
                "name": "string",
                "status": "string",
                "grade_weight": "decimal",
                "expected_grade": "decimal",
                "grade_result": "decimal",
                "delivery_date": "datetime",
                "discipline": "integer",
                "created_at": "datetime",
                "updated_at": "datetime"
            }
        ]
        ```
*   **`GET /api/activities/{id}/`**: Retrieve an activity.
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "status": "string",
            "grade_weight": "decimal",
            "expected_grade": "decimal",
            "grade_result": "decimal",
            "delivery_date": "datetime",
            "discipline": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`PUT /api/activities/{id}/`**: Update an activity.
    *   **Request Body**:
        ```json
        {
            "name": "string",
            "status": "string",
            "grade_weight": "decimal",
            "expected_grade": "decimal",
            "grade_result": "decimal",
            "delivery_date": "datetime",
            "discipline": "integer"
        }
        ```
    *   **Response Body**:
        ```json
        {
            "id": "integer",
            "name": "string",
            "status": "string",
            "grade_weight": "decimal",
            "expected_grade": "decimal",
            "grade_result": "decimal",
            "delivery_date": "datetime",
            "discipline": "integer",
            "created_at": "datetime",
            "updated_at": "datetime"
        }
        ```
*   **`DELETE /api/activities/{id}/`**: Delete an activity.
