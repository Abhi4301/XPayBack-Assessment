# models.py

class User:
    def __init__(self, first_name: str, email: str, password: str, phone: str):
        self.first_name = first_name
        self.email = email
        self.password = password
        self.phone = phone

class Profile:
    def __init__(self, email: str, profile_picture: bytes):
        self.email = email
        self.profile_picture = profile_picture
