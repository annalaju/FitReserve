from pydantic import BaseModel
from datetime import datetime
from typing import List


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


class FitnessClassBase(BaseModel):
    name: str
    dateTime: datetime
    instructor: str
    availableSlots: int


class FitnessClassCreate(FitnessClassBase):
    pass


class FitnessClassResponse(FitnessClassBase):
    id: int

    class Config:
        orm_mode = True


class BookingBase(BaseModel):
    class_id: int
    client_name: str
    client_email: str


class BookingCreate(BookingBase):
    pass


class BookingResponse(BookingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
