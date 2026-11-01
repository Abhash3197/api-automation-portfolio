import copy

import pytest

from config.settings import VALID_BOOKING


def _booking():
    return copy.deepcopy(VALID_BOOKING)


# NOTE: Restful-Booker has no input validation. Missing required fields cause an
# unhandled server error (500) instead of a 400. These tests pin that observed
# behaviour so a change (e.g. a fix to 400) is noticed.
@pytest.mark.smoke
@pytest.mark.parametrize("missing", ["firstname", "lastname", "totalprice", "bookingdates"])
def test_create_booking_missing_required_field(api_client, missing):
    booking = _booking()
    del booking[missing]

    response = api_client.post("/booking", booking)
    assert response.status_code == 500, f"Missing {missing}: got {response.status_code}"


@pytest.mark.smoke
def test_create_booking_missing_checkin(api_client):
    booking = _booking()
    booking["bookingdates"] = {"checkout": "2025-01-10"}

    response = api_client.post("/booking", booking)
    assert response.status_code == 500


@pytest.mark.smoke
def test_create_booking_with_zero_price(api_client):
    booking = _booking()
    booking["totalprice"] = 0

    response = api_client.post("/booking", booking)
    assert response.status_code == 200
    assert response.json()["booking"]["totalprice"] == 0
    api_client.delete(f"/booking/{response.json()['bookingid']}")


@pytest.mark.regression
def test_create_booking_with_negative_price_is_accepted(api_client):
    """Known gap: API accepts negative prices (should be 400)."""
    booking = _booking()
    booking["totalprice"] = -100

    response = api_client.post("/booking", booking)
    assert response.status_code == 200
    assert response.json()["booking"]["totalprice"] == -100
    api_client.delete(f"/booking/{response.json()['bookingid']}")


@pytest.mark.regression
def test_get_nonexistent_booking(api_client):
    assert api_client.get("/booking/99999999").status_code == 404


@pytest.mark.regression
def test_delete_nonexistent_booking(api_client):
    """With a valid token the API answers 405 for an unknown id."""
    assert api_client.delete("/booking/99999999").status_code == 405


@pytest.mark.regression
def test_update_without_token_is_forbidden(api_client, create_booking):
    import requests
    from config.settings import BASE_URL, UPDATED_BOOKING

    response = requests.put(f"{BASE_URL}/booking/{create_booking}", json=UPDATED_BOOKING, timeout=10)
    assert response.status_code == 403
