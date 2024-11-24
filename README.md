# Travel API with Microservices

## Overview
This project is a basic Travel API built with a microservices architecture using Flask. The API is divided into three main microservices:
1. **Destination Service**: Manages travel destinations.
2. **User Service**: Handles user registration, authentication, and profile management.
3. **Authentication Service**: Manages user authentication tokens and enforces role-based access.

Each microservice is independent and communicates over HTTP, adhering to OpenAPI standards with Swagger documentation for ease of use.

## Table of Contents
- [Features](#features)
- [Project Structure](#project-structure)
- [Endpoints](#endpoints)
- [Role-Based Access Control](#role-based-access-control)
- [Setup and Installation](#setup-and-installation)
- [Running Services](#running-services)
- [OpenAPI Documentation](#openapi-documentation)
- [Testing](#testing)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Features
- User registration, login, and profile management (Admins only for getting all profiles)
- View all travel destinations (Admins only for deletion and creation).
- Role-based access control for secure endpoints.
- Input validation and error handling.
- OpenAPI-compliant documentation using Swagger UI.
- Testing through Unittest
- Test Coverage of Each Foder up to 70%

## Project Structure

```

travel-api-project/
│
├── services/
│   ├── destination_service/
│   │   ├── tests
|   |   |    ├── test_app.py
|   |   |    └── test_destinations.py
│   │   ├── static
|   |   |    └── swagger.yaml
│   │   ├── init.py
│   │   ├── app.py
│   │   └──  destinations.py
│   │
│   ├── user_service/
│   │   ├── tests  
│   │   │     ├── test_app.py
│   │   │     └── test_users.py
│   │   ├── static
|   |   |     └── swagger.yaml
│   │   ├── init.py
│   │   ├── app.py
│   │   └── users.py
│   │
│   └── auth_service/
│       ├── tests  
│       │     ├── test_auth_app.py
│       │     └── test_auth.py
│       ├── static
|       |     └── swagger.yaml
│       ├── init.py
│       ├── app.py
│       └── auth.py
│
├── data/
│   ├── tests  
│   │     ├── test_destinations.py
│   │     └── test_users.py
│   ├── test_users_data.py'
│   ├── destinations_data.py
│   ├── users_data.py
│   ├── destinations.py
│   └── users.py
│
├── requirements.txt
└── README.md
```

## Endpoints

### **Destination Service**
| Method | Endpoint                       | Description                        | Access |
|--------|--------------------------------|------------------------------------|--------|
| GET    | `/destinations`                | Retrieve a list of all destinations | Public |
| POST   | `/destinations`                | Add a new destination               | Admin  |
| DELETE | `/destinations/<id>`           | Delete a specific destination       | Admin  |

**Destination Details**:
- **Name**: Destination name (string)
- **Description**: Short description (string)
- **Location**: Location name (string)

### **User Service**
| Method | Endpoint                       | Description                          | Access |
|--------|--------------------------------|--------------------------------------|--------|
| POST   | `/register`                    | Register a new user                  | Public |
| POST   | `/login`                       | Authenticate a user and get a token  | Public |
| GET    | `/profile`                     | View the current user's profile      | Authenticated |

**User Details**:
- **Name**: Full name (string)
- **Email**: Email address (string)
- **Password**: Hashed password (string)
- **Role**: User role ("Admin" or "User")
- **Admin Secret Key**: Admin secret key to register as admin role.

### **Authentication Service**
Handles user authentication and role-based access to endpoints.

## Role-Based Access Control

- Admin: Full access to all endpoints, including the ability to register and login as admin, get all users, post and delete destinations.

- User: Limited access, mainly for registration, login, viewing destinations and managing personal profiles.

- Token Authentication: All authenticated requests require a Bearer Token in the Authorization header.

## Setup and Installation

### Prerequisites
- Python 3.8 or higher
- Flask
- Flask-RESTful
- Flask-JWT-Extended
- Swagger-UI
- Virtualenv (recommended)

### Installation Steps

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Khairun-Nahar-Munne/Travel_API_Project.git
   cd travel-api-microservices
   ```

2. **Create Virtual Environment**:

   ```bash
   python3 -m venv myenv
   ```

3. **Activate Virtual Environment**:

   On Linux:
      ```bash
      source myenv/bin/activate
   ```
   On Windows:
      ```bash
   myenv\Scripts\activate
   ```
4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
      ```
 
## Running Services

### **User Service**
 ```bash
   cd services
   cd user_service
   python3 app.py
   ```

### **Authentication Service**
 ```bash
   cd services
   cd destination_service
   python3 app.py
   ```

### **Destination Service**
 ```bash
   cd services
   cd destination_service
   python3 app.py
   ```
## OpenAPI documentation 
OpenAI documenation is available through Swagger UI for each service:


- User Service: http://127.0.0.1:5002/docs/

   To register as an admin, you have to put  "Admin" in role property field and "your_admin_secret_key_here" in  admin_secret_key property field. After login, you will get authentication token. To get all profiles, you have to put this authentication token in authorize filed and login with this token as admin. 

   To register as an user, you have to put "User" in role property field.  After login, you will get authentication token. To get own profile, you have to put this authentication token in authorize filed and login with this token as user. 

- Authentication Service: http://127.0.0.1:5003/docs/

   After login in user service, you will get authentication token. To view own role, you have to put this authentication token in authorize filed and login with this token. You can view your role. 

- Destination Service: http://127.0.0.1:5001/docs/

   After login in user service, you will get authentication token. To view all destinations, you have to put this authentication token in authorize field and login with this token. 

   Admin can also post destinations and delete any destination through the id of the destinqation.

## Testing

To test the services, run the test suite using unittest. Each microservice includes a test folder named tests. To execute the test suite, navigate to the root directory of the project in your terminal window and enter:

### **User Service**

 ```bash
   python3 -m unittest discover -s services/user_service/tests
   ```

  For Coverage report:
   ```bash
   - coverage run -m unittest discover -s services/user_service/tests
   - coverage report
   ```

### **Authentication Service**

 ```bash
   python3 -m unittest discover -s services/auth_service/tests
   ```

  For Coverage report:
   ```bash
   - coverage run -m unittest discover -s services/auth_service/tests
   - coverage report
   ```


### **Destination Service**

   ```bash
   python3 -m unittest discover -s services/destination_service/tests
   ```

  For Coverage report:
   ```bash
   - coverage run -m unittest discover -s services/destination_service/tests
   - coverage report
   ```
### **Data**

   ```bash
   python3 -m unittest discover -s data/tests
   ```

  For Coverage report:
   ```bash
   - coverage run -m unittest discover -s data/tests
   - coverage report
   ```
## Error Handling

- Input validation for all endpoints.
- Custom error messages for missing fields, invalid inputs, and unauthorized access.
- 404 Not Found for non-existent resources.
- 400 Bad Request for invalid data formats

## Contributing
Contributions are welcome! Here's how you can contribute:

### Fork the Repository
```bash
- git clone https://github.com/Khairun-Nahar-Munne/Travel_API_Project.git
- cd Travel_API_Project
```
### Create a New Branch

```bash
- git checkout -b feature/add-new-feature
```
### Make Modifications and Commit Changes
```bash
- git commit -m 'Add new feature: [brief description of the feature]'

```
### Push Changes to the Branch

```bash
- git push origin feature/add-new-feature

```
### Create a New Pull Request
- Navigate to the repository on GitHub.
- Click on the "Compare & pull request" button.
- Fill in the pull request details and submit it for review.
