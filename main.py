# main.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timezone
from pytz import timezone as pytz_timezone

import models, schemas
from database import Base, engine, SessionLocal
from auth import get_current_user, create_access_token, get_password_hash, authenticate_user

# ----------------- INITIAL SETUP -----------------
Base.metadata.create_all(bind=engine)
app = FastAPI(title="Fitness Classes API")

# Timezone
IST = pytz_timezone("Asia/Kolkata")

# ----------------- DB DEPENDENCY -----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ----------------- AUTHENTICATION -----------------
@app.post("/signup/", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    if db.query(models.User).filter(models.User.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_pw = get_password_hash(user.password)
    new_user = models.User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.post("/login/")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

# ----------------- FITNESS CLASSES -----------------
@app.post("/classes/", response_model=schemas.FitnessClassResponse)
def create_class(
    fitness_class: schemas.FitnessClassCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Convert IST datetime input to UTC for storage
    dt_ist = fitness_class.dateTime.replace(tzinfo=IST)
    dt_utc = dt_ist.astimezone(timezone.utc)

    new_class = models.FitnessClass(
        name=fitness_class.name,
        dateTime=dt_utc,
        instructor=fitness_class.instructor,
        availableSlots=fitness_class.availableSlots
    )
    db.add(new_class)
    db.commit()
    db.refresh(new_class)
    return new_class

@app.get("/classes/", response_model=List[schemas.FitnessClassResponse])
def get_classes(db: Session = Depends(get_db)):
    classes = db.query(models.FitnessClass).all()
    # Convert UTC datetime to IST for response
    for cls in classes:
        if cls.dateTime.tzinfo is None:
            cls.dateTime = cls.dateTime.replace(tzinfo=timezone.utc)
        cls.dateTime = cls.dateTime.astimezone(IST)
    return classes

# ----------------- BOOKINGS -----------------
@app.post("/bookings/", response_model=schemas.BookingResponse)
def create_booking(
    booking: schemas.BookingCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    fitness_class = db.query(models.FitnessClass).filter(models.FitnessClass.id == booking.class_id).first()
    if not fitness_class:
        raise HTTPException(status_code=404, detail="Fitness class not found")
    if fitness_class.availableSlots <= 0:
        raise HTTPException(status_code=400, detail="No slots available")

    # Prevent duplicate booking
    existing_booking = db.query(models.Booking).filter(
        models.Booking.class_id == booking.class_id,
        models.Booking.user_id == current_user.id
    ).first()
    if existing_booking:
        raise HTTPException(status_code=400, detail="You already booked this class")

    new_booking = models.Booking(
        class_id=booking.class_id,
        client_name=booking.client_name,
        client_email=booking.client_email,
        user_id=current_user.id
    )

    fitness_class.availableSlots -= 1
    db.add(new_booking)
    db.commit()
    db.refresh(new_booking)
    return new_booking

@app.get("/bookings/", response_model=List[schemas.BookingResponse])
def get_bookings(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.Booking).filter(models.Booking.user_id == current_user.id).all()
