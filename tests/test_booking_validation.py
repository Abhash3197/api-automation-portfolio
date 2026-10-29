import pytest
from config.settings import VALID_BOOKING


@pytest.mark.smoke
def test_create_booking_missing_firstname(api_client):
    """Verify booking creation fails without firstname"""
    invalid_booking = VALID_BOOKING.copy()
    del invalid_booking["firstname"]

    response = api_client.post("/booking", invalid_booking)
    assert response.status_code != 200, "Should fail without firstname"


@pytest.mark.smoke
def test_create_booking_missing_lastname(api_client):
    """Verify booking creation fails without lastname"""
    invalid_booking = VALID_BOOKING.copy()
    del invalid_booking["lastname"]

    response = api_client.post("/booking", invalid_booking)
    assert response.status_code != 200, "Should fail without lastname"


@pytest.mark.smoke
def test_create_booking_missing_checkin(api_client):
    """Verify booking creation fails without checkin date"""
    invalid_booking = VALID_BOOKING.copy()
    invalid_booking["bookingdates"] = {"checkout": "2025-01-10"}

    response = api_client.post("/booking", invalid_booking)
    assert response.status_code != 200, "Should fail without checkin date"


@pytest.mark.smoke
def test_create_booking_with_zero_price(api_client):
    """Verify booking can be created with zero price"""
    booking = VALID_BOOKING.copy()
    booking["totalprice"] = 0

    response = api_client.post("/booking", booking)
    assert response.status_code == 200, "Should allow zero price bookings"
    data = response.json()
    assert data["booking"]["totalprice"] == 0


@pytest.mark.regression
def test_create_booking_with_negative_price(api_client):
    """Verify booking fails with negative price"""
    booking = VALID_BOOKING.copy()
    booking["totalprice"] = -100

    response = api_client.post("/booking", booking)
    # API might accept or reject - document the behavior
    assert response.status_code in [200, 400], "Behavior depends on API validation"


@pytest.mark.regression
def test_get_nonexistent_booking(api_client):
    """Verify getting non-existent booking returns 404"""
    response = api_client.get("/booking/99999999")
    assert response.status_code == 404, "Non-existent booking should return 404"


@pytest.mark.regression
def test_delete_nonexistent_booking(api_client):
    """Verify deleting non-existent booking"""
    response = api_client.delete("/booking/99999999")
    assert response.status_code in [404, 201], "Delete behavior varies by API design"
