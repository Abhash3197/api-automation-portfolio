import pytest
from api_client import APIClient
from config.settings import BASE_URL, VALID_BOOKING


@pytest.fixture
def api_client():
    client = APIClient(BASE_URL)
    yield client
    client.close()


@pytest.fixture
def booking_data():
    return VALID_BOOKING.copy()


@pytest.fixture
def create_booking(api_client):
    """Fixture to create a booking and return booking ID"""
    response = api_client.post("/booking", VALID_BOOKING)
    if response.status_code == 200:
        booking_id = response.json().get("bookingid")
        yield booking_id
        # Cleanup: delete the booking
        api_client.delete(f"/booking/{booking_id}")
    else:
        yield None
