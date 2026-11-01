# API Automation Portfolio — Restful-Booker

![API Tests](https://github.com/Abhash3197/api-automation-portfolio/actions/workflows/tests.yml/badge.svg)

API test suite built with **pytest + requests + jsonschema** against the public [Restful-Booker](https://restful-booker.herokuapp.com) API. The suite checks contract, auth and error behaviour, and it records where the API departs from good REST practice.

## Results

23 tests (smoke and regression), all passing, about 8 seconds with `-n 4`.

| Suite | Tests | Covers |
|---|---|---|
| `test_booking_crud.py` | 5 | create, get, update, delete, list |
| `test_schema.py` | 3 | JSON-schema contract for create / get / list responses |
| `test_booking_filters.py` | 5 | filter by first/last name, check-in/out, unknown params |
| `test_booking_validation.py` | 10 | missing fields, edge values, 404/405, missing-token 403 |

## Findings (API behaviour the tests pin down)

Restful-Booker is a deliberately imperfect target. These tests assert the **observed** behaviour, so a change to it fails the suite.

| Behaviour | Observed | Expected for a well-behaved API |
|---|---|---|
| POST with a missing required field (`firstname`, `lastname`, `totalprice`, `bookingdates`, or `checkin`) | `500` | `400` with an error message |
| POST with `totalprice: -100` | `200`, stored as-is | `400` |
| DELETE of a non-existent id (with a valid token) | `405` | `404` |
| PUT without a token | `403` | `401` / `403` |
| GET with an unknown query parameter | `200`, filter ignored | `200` or `400` |

## Quick start

```bash
git clone https://github.com/Abhash3197/api-automation-portfolio.git
cd api-automation-portfolio
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

pytest tests/ -m smoke -v          # core flows
pytest tests/ -n auto              # everything, in parallel
pytest tests/ --html=reports/report.html --self-contained-html
```

## Structure

```
api_client.py      requests.Session wrapper; fetches an auth token lazily for PUT/PATCH/DELETE
schemas.py         JSON schemas for booking responses
config/settings.py base URL, timeout, test payloads (env-overridable)
tests/             conftest fixtures + test modules
```

## Design decisions

- **Fixtures own test data.** `create_booking` creates a booking and deletes it on teardown. Tests that create bookings inline clean up after themselves, so the shared public API doesn't fill up with junk.
- **Schema validation on responses.** Status-code checks alone miss contract drift (a field that changes type, a missing key). `jsonschema` covers that.
- **Pin real behaviour, don't guess.** I probed the API first and then wrote the exact status codes into the assertions. My first draft used loose `in [200, 400]` checks, which couldn't catch regressions, so I replaced them.
- **Markers.** `smoke` covers the critical flows, and `regression` covers edge cases and known-gap tests.
- **Parallel-safe.** Each test creates its own data, so `pytest -n auto` is safe.

## Limitations

- The target is a shared public service. It can be slow or reset, and other users' data appears in list calls.
- `PATCH` isn't covered by tests yet.
- There are no performance or response-time assertions.
- The auth token is fetched once per client, with no expiry handling.

## CI

GitHub Actions runs the full suite in parallel on every push and PR to `main`/`master`. It uploads the HTML report as an artifact.
