import pytest
from jsonschema import validate

from config.settings import VALID_BOOKING
from schemas import BOOKING_LIST_SCHEMA, BOOKING_SCHEMA, CREATE_BOOKING_SCHEMA


@pytest.mark.smoke
def test_create_booking_response_schema(api_client):
    response = api_client.post("/booking", VALID_BOOKING)
    assert response.status_code == 200
    body = response.json()
    validate(instance=body, schema=CREATE_BOOKING_SCHEMA)
    api_client.delete(f"/booking/{body['bookingid']}")


@pytest.mark.smoke
def test_get_booking_response_schema(create_booking, api_client):
    response = api_client.get(f"/booking/{create_booking}")
    assert response.status_code == 200
    validate(instance=response.json(), schema=BOOKING_SCHEMA)


@pytest.mark.smoke
def test_list_bookings_response_schema(api_client):
    response = api_client.get("/booking")
    assert response.status_code == 200
    validate(instance=response.json(), schema=BOOKING_LIST_SCHEMA)
