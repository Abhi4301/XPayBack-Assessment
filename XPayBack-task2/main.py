from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse
import base64
from typing import Optional
import schemas
import database
import models
import utils


App = FastAPI()

# Dependency to get the PostgreSQL connection
def get_db():
    db = database.get_postgresql_connection()
    try:
        yield db
    finally:
        db.close()

# Ensure tables exist
def init_db():
    db = database.get_postgresql_connection()
    cursor = db.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        first_name VARCHAR(50),
        email VARCHAR(255) PRIMARY KEY,
        password TEXT,
        phone VARCHAR(20) UNIQUE
    );
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Profile (
        email VARCHAR(255) PRIMARY KEY,
        profile_picture BYTEA,
        FOREIGN KEY (email) REFERENCES Users (email)
    );
    """)
    db.commit()
    cursor.close()
    db.close()

init_db()

@App.post("/register", response_model=schemas.MessageResponse)
async def register_user(
    full_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(...),
    profile_picture: Optional[UploadFile] = File(None),
    db = Depends(get_db)
):
    # Extract first name from full name
    first_name = full_name.split()[0] if full_name else None

    cursor = db.cursor()

    # Check if the email or phone already exists in PostgreSQL
    cursor.execute("SELECT email FROM Users WHERE email = %s", (email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    cursor.execute("SELECT phone FROM Users WHERE phone = %s", (phone,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Phone already registered")

    # Hash the password before storing it
    hashed_password = utils.hash_password(password)

    # Handle profile picture
    profile_picture_data = None
    if profile_picture:
        profile_picture_data = await profile_picture.read()

    # Save user details in PostgreSQL
    new_user = models.User(
        first_name=first_name,
        email=email,
        password=hashed_password,  # Store the hashed password
        phone=phone
    )

    try:
        cursor.execute(
            "INSERT INTO Users (first_name, email, password, phone) VALUES (%s, %s, %s, %s)",
            (new_user.first_name, new_user.email, new_user.password, new_user.phone)
        )
        db.commit()

        if profile_picture_data:
            # Store the profile picture in the Profile table
            cursor.execute(
                "INSERT INTO Profile (email, profile_picture) VALUES (%s, %s) ON CONFLICT (email) DO UPDATE SET profile_picture = EXCLUDED.profile_picture",
                (new_user.email, profile_picture_data)
            )
            db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to register user")
    
    cursor.close()
    return {"message": "Registration successful"}

@App.get("/user/{email}")
async def get_user(email: str, db = Depends(get_db)):
    cursor = db.cursor()

    # Fetch user details from PostgreSQL
    cursor.execute("""
        SELECT u.first_name, u.email, u.phone, p.profile_picture
        FROM Users u
        LEFT JOIN Profile p ON u.email = p.email
        WHERE u.email = %s
    """, (email,))
    
    user_data = cursor.fetchone()

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    first_name = user_data['first_name']
    email = user_data['email']
    phone = user_data['phone']
    profile_picture_data = user_data['profile_picture']

    # Convert profile_picture_data to base64
    profile_picture = None
    if profile_picture_data:
        try:
            # Ensure profile_picture_data is bytes
            if isinstance(profile_picture_data, memoryview):
                profile_picture_data = profile_picture_data.tobytes()
            elif isinstance(profile_picture_data, str):
                profile_picture_data = profile_picture_data.encode('utf-8')

            image_base64 = base64.b64encode(profile_picture_data).decode('utf-8')
            profile_picture = f"data:image/jpeg;base64,{image_base64}"

        except Exception as e:
            raise HTTPException(status_code=500, detail="Error encoding image data")

    return JSONResponse(content={
        "first_name": first_name,
        "email": email,
        "phone": phone,
        "profile_picture": profile_picture
    })