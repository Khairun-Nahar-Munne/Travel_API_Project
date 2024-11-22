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
- [Setup and Installation](#setup-and-installation)
- [Running the Services](#running-the-services)
- [Testing](#testing)
- [API Documentation](#api-documentation)
- [Role-Based Access Control](#role-based-access-control)
- [Error Handling](#error-handling)
- [Contributing](#contributing)

## Features
- User registration, login, and profile management.
- CRUD operations for travel destinations (Admins only for deletion).
- Role-based access control for secure endpoints.
- Input validation and error handling.
- OpenAPI-compliant documentation using Swagger UI.

## Project Structure

```

travel-microservices/
│
├── services/
│   ├── destination_service/
│   │   ├── init.py
│   │   ├── app.py
│   │   ├── destinations.py
│   │   └── swagger.yaml
│   │
│   ├── user_service/
│   │   ├── init.py
│   │   ├── app.py
│   │   ├── users.py
│   │   └── swagger.yaml
│   │
│   └── auth_service/
│       ├── init.py
│       ├── app.py
│       ├── auth.py
│       └── swagger.yaml
│
├── data/
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

### **Authentication Service**
Handles user authentication and role-based access to endpoints.

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
   git clone https://github.com/yourusername/travel-api-microservices.git
   cd travel-api-microservices
