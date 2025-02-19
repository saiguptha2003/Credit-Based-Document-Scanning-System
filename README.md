# Credit-Based Document Scanning System

This system allows users to scan documents and manage credits associated with the scanning process. Users can request credits, which can be approved or rejected by administrators. The system tracks user activity, including the number of scans and credit usage, while ensuring that only non-admin users are included in the statistics.

## Features
- User authentication and authorization
- Credit management for document scanning
- Admin dashboard for monitoring requests and user statistics
- Analytics for document scanning activity

## Installation
Instructions for setting up the project locally.

To set up the project locally, follow one of the methods below:

### Clone the Repository
You can clone the repository using Git:

```bash
git clone https://github.com/saiguptha2003/Credit-Based-Document-Scanning-System.git
cd Credit-Based-Document-Scanning-System
```
### Docker Compose Installation
1. Ensure you have Docker Compose installed. You can find installation instructions [here](https://docs.docker.com/compose/install/).
2. In the project directory, run:
   ```bash
   docker-compose up
   ```
3. Build the Docker containers with detach and build options:
    ```bash
    docker-compose up --build -d
    ```
4. Access the application at `http://localhost:5000`

### Manual Installation
1. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
2. Activate the virtual environment:
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```
   - On Unix or MacOS:  
     ```bash
     source venv/bin/activate
     ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables:
   - Create a `.env` file in the project root:
     ```bash
     touch .env
     ```
5. Run the development server:
   ```bash
   python main.py
   ```
6. Access the application at `http://localhost:5000`

### Dockerfile Installation
1. Ensure you have Docker installed. You can find installation instructions [here](https://docs.docker.com/get-docker/).
2. Build the Docker image:
   ```bash
   docker build -t document-scanner .
   ```
3. Run the Docker container:
   ```bash
   docker run -p 5000:5000 document-scanner
   ```
4. Access the application at `http://localhost:5000`

## Usage

### API Routes

#### 1. Dashboard Route
- **Endpoint:** `/api/scan/dashboard`
- **Method:** `GET`
- **Description:** Retrieves the user's dashboard information, including their username, credits, documents, and credit requests.
- **Request Body:** None
- **Response:**
  - **Status Code:** `200 OK`
  - **Response Body:**
    ```json
    {
        "user": {
            "username": "string",
            "credits": "integer"
        },
        "documents": [
            {
                "id": "integer",
                "title": "string",
                "created_at": "string"
            }
        ],
        "credit_requests": [
            {
                "id": "integer",
                "amount": "integer",
                "status": "string",
                "created_at": "string"
            }
        ]
    }
    ```

#### 2. Scan Document Route
- **Endpoint:** `/api/scan/scan-document`
- **Method:** `POST`
- **Description:** Allows users to upload a document (PDF or TXT) for scanning. The document's content is processed, and similarity with existing documents is checked.
- **Request Body:**
  - **Form Data:**
    - `file`: The document file to be scanned (must be of type PDF or TXT).
- **Response:**
  - **Status Code:** `200 OK` (on success) or `400 Bad Request` / `403 Forbidden` / `500 Internal Server Error` (on error)
  - **Response Body (Success):**
    ```json
    {
        "message": "Document scanned successfully",
        "document": {
            "id": "integer",
            "title": "string",
            "content": "string",
            "created_at": "string",
            "user_id": "integer",
            "similarity": "float"
        },
        "similar_documents": [
            {
                "id": "integer",
                "title": "string",
                "content": "string",
                "created_at": "string",
                "user_id": "integer",
                "similarity": "float"
            }
        ]
    }
    ```

#### 3. Request Credits Route
- **Endpoint:** `/api/scan/request-credits`
- **Method:** `POST`
- **Description:** Allows users to request additional credits.
- **Request Body:**
  - **JSON:**
    ```json
    {
        "amount": "integer"
    }
    ```
- **Response:**
  - **Status Code:** `201 Created` (on success) or `400 Bad Request` (on error)
  - **Response Body (Success):**
    ```json
    {
        "message": "Credit request submitted",
        "request": {
            "id": "integer",
            "amount": "integer",
            "status": "string",
            "created_at": "string"
        }
    }
    ```


#### 4. Find Similar Documents
- **Endpoint:** This is an internal function and does not have a direct route.
- **Method:** N/A
- **Description:** Compares the uploaded document's content with existing documents to find similar ones based on a defined similarity threshold.
- **Request Body:** N/A
- **Response:** Returns a list of similar documents with their similarity scores.

#### 1. Admin Dashboard Route
- **Endpoint:** `/api/admin/dashboard`
- **Method:** `GET`
- **Description:** Retrieves the admin dashboard data, including pending credit requests and user statistics.
- **Response:**
  - **Status Code:** `200 OK` (on success) or `500 Internal Server Error` (on error)
  - **Response Body (Success):**
    ```json
    {
        "pending_requests": [
            {
                "id": "integer",
                "user_id": "integer",
                "amount": "integer",
                "created_at": "string"
            }
        ],
        "users": [
            {
                "id": "integer",
                "username": "string",
                "credits": "integer",
                "document_count": "integer"
            }
        ],
        "total_documents": "integer"
    }
    ```

#### 2. Handle Credit Request Route
- **Endpoint:** `/api/admin/credit-requests/<int:request_id>`
- **Method:** `PUT`
- **Description:** Approves or rejects a credit request based on the action specified in the request body.
- **Request Body:**
  - **JSON:**
    ```json
    {
        "action": "string"  // "approve" or "reject"
    }
    ```
- **Response:**
  - **Status Code:** `200 OK` (on success) or `400 Bad Request` (on invalid action) or `500 Internal Server Error` (on error)
  - **Response Body (Success):**
    ```json
    {
        "message": "Credit request approved/rejected",
        "request": {
            "id": "integer",
            "status": "string",
            "processed_at": "string"
        }
    }
    ```

#### 3. Analytics Route
- **Endpoint:** `/api/admin/analytics`
- **Method:** `GET`
- **Description:** Retrieves user statistics, credit statistics, and document statistics for the admin.
- **Response:**
  - **Status Code:** `200 OK` (on success) or `500 Internal Server Error` (on error)
  - **Response Body (Success):**
    ```json
    {
        "user_statistics": [
            {
                "username": "string",
                "scan_count": "integer"
            }
        ],
        "credit_statistics": [
            {
                "username": "string",
                "credits": "integer"
            }
        ],
        "document_statistics": [
            {
                "extension": "string",
                "count": "integer"
            }
        ]
    }
    ```

## Contributing
Guidelines for contributing to the project.

## License
Information about the project's license.
