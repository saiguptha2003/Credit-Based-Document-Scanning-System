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
How to use the system after installation.

## Contributing
Guidelines for contributing to the project.

## License
Information about the project's license.
