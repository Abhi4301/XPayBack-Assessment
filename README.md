# XPayBack-Assessment - FastAPI User Management Project

## Overview

This project is a FastAPI application designed to manage user registrations and details. It features two distinct tasks:

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
