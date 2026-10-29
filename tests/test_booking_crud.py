import pytest
from config.settings import VALID_BOOKING, UPDATED_BOOKING


@pytest.mark.smoke
def test_create_booking(api_client):
    """Verify booking creation"""
    response = api_client.post("/booking", VALID_BOOKING)

    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    data = response.json()
    assert "bookingid" in data, "Response should contain bookingid"
    assert data["booking"]["firstname"] == VALID_BOOKING["firstname"]
    assert data["booking"]["lastname"] == VALID_BOOKING["lastname"]
    assert data["booking"]["totalprice"] == VALID_BOOKING["totalprice"]


@pytest.mark.smoke
def test_get_booking(create_booking, api_client):
    """Verify retrieving a booking by ID"""
    booking_id = create_booking
    response = api_client.get(f"/booking/{booking_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == VALID_BOOKING["firstname"]
    assert data["lastname"] == VALID_BOOKING["lastname"]


@pytest.mark.smoke
def test_update_booking(create_booking, api_client):
    """Verify updating a booking"""
    booking_id = create_booking

    response = api_client.put(
        f"/booking/{booking_id}",
        UPDATED_BOOKING,
        headers={"Content-Type": "application/json"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["firstname"] == UPDATED_BOOKING["firstname"]
    assert data["lastname"] == UPDATED_BOOKING["lastname"]
    assert data["totalprice"] == UPDATED_BOOKING["totalprice"]


@pytest.mark.smoke
def test_delete_booking(create_booking, api_client):
    """Verify deleting a booking"""
    booking_id = create_booking

    # Verify booking exists
    response = api_client.get(f"/booking/{booking_id}")
    assert response.status_code == 200

    # Delete booking
    response = api_client.delete(f"/booking/{booking_id}")
    assert response.status_code == 201, "Delete should return 201"

    # Verify booking is deleted
    response = api_client.get(f"/booking/{booking_id}")
    assert response.status_code == 404, "Deleted booking should return 404"


@pytest.mark.smoke
def test_list_bookings(api_client):
    """Verify listing all bookings"""
    response = api_client.get("/booking")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Response should be a list"
    assert len(data) > 0, "Should have at least one booking"
    assert "bookingid" in data[0], "Each booking should have bookingid"
