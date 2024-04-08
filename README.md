# Library Management API

## Overview
This API provides endpoints for managing student records in a library system. It allows CRUD operations for students' data.

## API Documentation
The detailed API documentation can be found [here](https://documenter.getpostman.com/view/23687971/2sA35Myz41).

## Technologies Used
- Python
- FastAPI
- MongoDB

## Installation and Setup
1. Clone the repository.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Set up your MongoDB URI in the `.env` file.
4. Run the API using `uvicorn main:app --reload`.

## Endpoints
- **GET /students**: Retrieve a list of all students.
- **GET /students/{id}**: Retrieve details of a specific student.
- **POST /students**: Create a new student record.
- **PATCH /students/{id}**: Update an existing student record.
- **DELETE /students/{id}**: Delete a student record.

## Usage
1. Ensure the API is running locally or deployed.
2. Use tools like Postman or cURL to send requests to the API endpoints.
3. Follow the API documentation for request formats and responses.

## Contributing
Contributions are welcome! Please follow the contribution guidelines outlined in CONTRIBUTING.md.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

