import os
from dotenv import load_dotenv

load_dotenv()

# Restful-Booker API
BASE_URL = os.getenv("BASE_URL", "https://restful-booker.herokuapp.com")
TIMEOUT = int(os.getenv("TIMEOUT", 10))

# Test data
VALID_BOOKING = {
    "firstname": "John",
    "lastname": "Doe",
    "totalprice": 111,
    "depositpaid": True,
    "bookingdates": {
        "checkin": "2025-01-01",
        "checkout": "2025-01-10"
    },
    "additionalneeds": "Breakfast"
}

UPDATED_BOOKING = {
    "firstname": "Jane",
    "lastname": "Smith",
    "totalprice": 200,
    "depositpaid": False,
    "bookingdates": {
        "checkin": "2025-02-01",
        "checkout": "2025-02-10"
    },
    "additionalneeds": "Late checkout"
}
