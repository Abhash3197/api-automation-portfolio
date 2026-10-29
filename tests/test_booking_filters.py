import pytest
from config.settings import VALID_BOOKING


@pytest.mark.smoke
def test_list_bookings_with_name_filter(api_client, create_booking):
    """Verify filtering bookings by firstname"""
    response = api_client.get(
        "/booking",
        params={"firstname": VALID_BOOKING["firstname"]}
    )

    assert response.status_code == 200
    data = response.json()
    if len(data) > 0:
        assert isinstance(data, list), "Filtered result should be a list"


@pytest.mark.smoke
def test_list_bookings_with_lastname_filter(api_client, create_booking):
    """Verify filtering bookings by lastname"""
    response = api_client.get(
        "/booking",
        params={"lastname": VALID_BOOKING["lastname"]}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Filtered result should be a list"


@pytest.mark.smoke
def test_list_bookings_with_checkin_filter(api_client, create_booking):
    """Verify filtering bookings by checkin date"""
    checkin_date = VALID_BOOKING["bookingdates"]["checkin"]
    response = api_client.get(
        "/booking",
        params={"checkin": checkin_date}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Filtered result should be a list"


@pytest.mark.smoke
def test_list_bookings_with_checkout_filter(api_client, create_booking):
    """Verify filtering bookings by checkout date"""
    checkout_date = VALID_BOOKING["bookingdates"]["checkout"]
    response = api_client.get(
        "/booking",
        params={"checkout": checkout_date}
    )

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list), "Filtered result should be a list"


@pytest.mark.regression
def test_list_bookings_with_invalid_filter(api_client):
    """Verify API handles invalid filter parameters"""
    response = api_client.get(
        "/booking",
        params={"invalid_param": "value"}
    )

    # API should either ignore or handle gracefully
    assert response.status_code in [200, 400], "Should handle invalid filters gracefully"
