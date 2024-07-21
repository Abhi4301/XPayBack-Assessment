# XPayBack-Assessment - FastAPI User Management Project

## Overview

This project contains two FastAPI applications that provide endpoints for managing users. The first application uses two databases (PostgreSQL and MongoDB) to store user data, while the second application uses a single PostgreSQL database.

- **Task 1:** Uses PostgreSQL for user details and MongoDB for storing profile pictures.
- **Task 2:** Uses a single PostgreSQL database for storing all user data, including profile pictures.

The application provides endpoints to register users and retrieve their details.

## Project Structure

```plaintext
XPayBack-Assessment
├── XPayBack-task1
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── XPayBack-task2
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── utils.py
├── README.md
└── requirements.txt
```
  

## Task Details

**Task 1: User Registration with PostgreSQL and MongoDB**
1. **User Registration Endpoint:**

- **Fields:** Full Name, Email, Password, Phone, Profile Picture
- **Storage:**
  - **PostgreSQL:** First Name, Password, Email, Phone
  - **MongoDB:** Profile Picture
  - **Validation:** Ensures the email does not already exist.

2. **User Details Retrieval Endpoint:**
  - **Method:** GET
  - **Description:** Retrieves details of a registered user.

**Task 2: User Registration with PostgreSQL**
1. **User Registration Endpoint:**
  - **Fields:** Full Name, Email, Password, Phone, Profile Picture
  - **Storage:**
    - **Users Table:** First Name, Password, Email, Phone
    - **Profile Table:** Profile Picture
  - **Validation:** Ensures the email and phone number do not already exist.   

2. **User Details Retrieval Endpoint:**
  - **Method:** GET
  - **Description:** Retrieves details of a registered user.


## Installation
1. **Clone the repository:**
```
git clone https://github.com/Abhi4301/XPayBack-Assessment.git
cd your-repo
```

2. **Create a virtual environment:**
```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. **Install the dependencies:**
```
pip install -r requirements.txt
```

4. **Set up the PostgreSQL and MongoDB databases:**

  - For Task 1, configure both PostgreSQL and MongoDB databases and ensure you have the connection details ready.
  - For Task 2, configure a single PostgreSQL database for both user details and profile pictures.

## Usage
1. **Run the FastAPI server:**
```
uvicorn XPayBack-task1.main:app --reload --port 8001  # For task 1
uvicorn XPayBack-task2.main:app --reload --port 8002  # For task 2
```

2. **Access the API:**
   Open your web browser and navigate to http://127.0.0.1:8000. You can also access the automatically generated API documentation at http://127.0.0.1:8000/docs.

## Endpoints
### POST /register
**Description:** Registers a new user.
  - Accepts form data with fields: full_name, email, password, phone, profile_picture.
  
  - **Request Body:**
  ```
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "password": "securepassword",
  "phone": "1234567890",
  "profile_picture": "base64_encoded_image_string"
}
  ```

- **Response:**
  - **200 OK:** User successfully registered.
  - **400 Bad Request:** Validation error (e.g., email already exists).
 
### GET /user/{email}
**Description:** Retrieves user details by email.

- **Path Parameters:**
  - **email (string):** The email address of the user.
- **Response:**
  - **200 OK:** Returns user details including the profile picture.
  - **404 Not Found:** User not found.
