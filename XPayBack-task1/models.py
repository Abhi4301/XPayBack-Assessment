# models.py

class User:
    def __init__(self, first_name: str, email: str, password: str, phone: str):
        self.first_name = first_name
        self.email = email
        self.password = password
        self.phone = phone