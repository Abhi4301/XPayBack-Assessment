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
