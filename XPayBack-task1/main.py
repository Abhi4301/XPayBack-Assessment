from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
import schemas
import database
import models
import utils
from typing import Optional
from fastapi.responses import JSONResponse
import base64

App = FastAPI()

# Dependency to get the PostgreSQL connection
def get_db():
    db = database.get_postgresql_connection()
    try:
        yield db
    finally:
        db.close()

@App.post("/register", response_model=schemas.UserResponse)
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

    # Check if the email already exists in PostgreSQL
    cursor = db.cursor()
    cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash the password before storing it
    hashed_password = utils.hash_password(password)
    
    # Save profile picture in MongoDB GridFS
    profile_picture_id = None
    if profile_picture:
        profile_picture_id = database.fs.put(await profile_picture.read(), filename=f"{email}_profile_picture")
    
    # Save user details in PostgreSQL
    new_user = models.User(
        first_name=first_name,
        email=email,
        password=hashed_password,  # Store the hashed password
        phone=phone
    )

    try:
        cursor.execute(
            "INSERT INTO users (first_name, email, password, phone) VALUES (%s, %s, %s, %s)",
            (new_user.first_name, new_user.email, new_user.password, new_user.phone)
        )
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to register user")

    # Save profile picture reference in MongoDB
    profile_document = {
        'email': new_user.email,
        'Profile_picture': profile_picture_id
    }
    database.profile_collection.insert_one(profile_document)

    return JSONResponse(content={"message": "Registration successful"})


@App.post("/login")
async def login_user(
    email: str = Form(...),
    password: str = Form(...),
    db = Depends(get_db)
):
    # Fetch user details from PostgreSQL
    cursor = db.cursor()
    cursor.execute("SELECT password FROM users WHERE email = %s", (email,))
    result = cursor.fetchone()
    
    if result is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    stored_hashed_password = result[0]
    
    # Verify the provided password against the stored hash
    if not utils.verify_password(password, stored_hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    return {"message": "Login successful"}


@App.get("/user/{email}")
async def get_user(email: str, db = Depends(get_db)):
    # Fetch user details from PostgreSQL
    cursor = db.cursor()
    cursor.execute("SELECT first_name, email, phone FROM users WHERE email = %s", (email,))
    user_data = cursor.fetchone()
    
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    first_name, email, phone = user_data

    # Fetch profile picture reference from MongoDB
    profile_document = database.profile_collection.find_one({'email': email})
    
    if profile_document and profile_document.get('Profile_picture'):
        # Fetch the image from GridFS
        image_id = profile_document['Profile_picture']
        image_data = database.fs.get(image_id).read()
        # Convert image data to base64
        image_base64 = base64.b64encode(image_data).decode('utf-8')
        profile_picture = f"data:image/jpeg;base64,{image_base64}"
    else:
        profile_picture = None

    # Return the user data along with the image data
    return JSONResponse(content={
        "first_name": first_name,
        "email": email,
        "phone": phone,
        "profile_picture": profile_picture
    })