FitReserve

A FastAPI-based backend API for managing fitness classes and bookings. Users can signup, login, create classes, book classes, and view their bookings. Authentication is handled via JWT tokens.
## Features

- User signup and login

- JWT-based authentication

- Create fitness classes (authenticated)

- View available classes

- Book classes (authenticated)

- View user bookings

- Prevent overbooking and duplicate bookings

- Handles timezones (IST/UTC)


## Tech Stack
- Python 3.12

- FastAPI

- SQLite

- SQLAlchemy ORM

- Pydantic

- JWT Authentication

- pytest for testing
## Setup Instructions
1. Clone the repository

git clone <your-repo-url>
cd fitness_booking_api


2. Create a virtual environment

python -m venv venv
source venv/bin/activate      # Linux / Mac
venv\Scripts\activate         # Windows


3. Install dependencies

pip install -r requirements.txt


4. Run the application

uvicorn main:app --reload


5. Open Swagger docs at:
http://127.0.0.1:8000/docs
## API Usage
1. Signup
POST /signup/
{
  "name": "Alice",
  "email": "alice@example.com",
  "password": "password123"
}

2. Login
POST /login/
Form-data:
username: alice@example.com
password: password123


Response:

{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}

3. Create a Class (Authenticated)
POST /classes/
Headers: Authorization: Bearer <JWT_TOKEN>
{
  "name": "Yoga Flow",
  "dateTime": "2025-09-01T10:00:00",
  "instructor": "John Doe",
  "availableSlots": 5
}

4. Get Classes
GET /classes/

5. Book a Class (Authenticated)
POST /bookings/
Headers: Authorization: Bearer <JWT_TOKEN>
{
  "class_id": 1,
  "client_name": "Alice",
  "client_email": "alice@example.com"
}

6. Get Bookings (Authenticated)
GET /bookings/
Headers: Authorization: Bearer <JWT_TOKEN>
## Running Tests
pytest


Tests include: signup, login, class creation, booking, and fetching bookings.
