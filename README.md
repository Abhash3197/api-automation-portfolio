# API Automation Portfolio — Restful-Booker

Production-grade API test automation suite using **pytest** and **requests**. Tests a real public API with CRUD operations, validation, and filtering.

**Target**: [Restful-Booker API](https://restful-booker.herokuapp.com) — A hotel booking API designed for testing.

## What This Tests

✅ **CRUD Operations** — Create, read, update, delete bookings  
✅ **Input Validation** — Required fields, invalid data, edge cases  
✅ **Filtering & Search** — Filter by date, name, checkout date  
✅ **Error Handling** — 404s, missing fields, invalid operations  

## Quick Start

### Prerequisites
- Python 3.11+
- pip

### Installation
```bash
git clone <repo>
cd api-automation-portfolio
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run Tests
```bash
# Smoke tests only (2-3 min)
pytest tests/ -m smoke -v

# Full suite (5-7 min)
pytest tests/ -v

# Parallel execution
pytest tests/ -v -n auto

# With HTML report
pytest tests/ -v --html=reports/report.html --self-contained-html
```

## Project Structure

```
api-automation-portfolio/
├── api_client.py           # HTTP client wrapper
├── config/
│   └── settings.py         # API base URL, test data
├── tests/
│   ├── conftest.py         # Pytest fixtures
│   ├── test_booking_crud.py         # Create/read/update/delete
│   ├── test_booking_validation.py   # Input validation, errors
│   └── test_booking_filters.py      # Search, filtering
├── requirements.txt
├── pytest.ini
└── .github/workflows/      # CI/CD
```

## Test Coverage

| Suite | Tests | Type | Purpose |
|-------|-------|------|---------|
| **CRUD** | 5 | Smoke | Create, get, update, delete, list |
| **Validation** | 4 | Smoke + Regression | Required fields, edge cases, errors |
| **Filters** | 5 | Smoke + Regression | Date filters, name filters, invalid params |
| **Total** | 14 | | End-to-end booking API flows |

## Architecture Decisions

### 1. **APIClient Wrapper**
- Centralized HTTP methods (GET, POST, PUT, DELETE)
- Session reuse for efficiency
- Configurable timeouts and headers
- Single point for adding auth, logging, retries

### 2. **Fixture-Based Setup/Teardown**
- `create_booking` fixture auto-cleans up test data
- `api_client` fixture manages session lifecycle
- Prevents test data pollution

### 3. **Test Markers (smoke/regression)**
- `@pytest.mark.smoke`: Core happy-path flows (13 tests, ~2 min)
- `@pytest.mark.regression`: Edge cases and error handling
- Smoke runs on every commit; regression nightly

### 4. **Test Data as Config**
- `VALID_BOOKING` and `UPDATED_BOOKING` in settings.py
- Single source of truth for test payloads
- Easy to adjust dates or values globally

## What Makes This Portfolio-Ready

✅ **Reproducible** — Clone, install, pytest → green in ~2 min  
✅ **Real API** — Tests against live Restful-Booker; results are verifiable  
✅ **Clean Code** — Minimal fixtures, clear test names, no fluff  
✅ **CRUD Expertise** — Shows understanding of REST principles  
✅ **Error Handling** — Documents API behavior (404s, validation)  
✅ **CI-Ready** — GitHub Actions on every push  

## Test Results

**Latest Run**:
- Tests: 14 total (13 smoke, 1 regression)
- Smoke: All passing (~2 min)
- Status: ✅ Green

## Known Limitations & Roadmap

- **No auth tests** — Restful-Booker doesn't require auth; add for real APIs
- **No schema validation** — Ready to add jsonschema assertions
- **No performance tests** — Could add response time baselines
- **No retry logic** — Would help with flaky networks

### Planned Enhancements
1. Add Bearer token auth header support
2. Schema validation for request/response payloads
3. Data-driven tests using `@pytest.mark.parametrize`
4. Custom assertions for common patterns (status checks, field presence)
5. Allure reporting for trend analysis

## Local Development

```bash
# Run with verbose output
pytest tests/test_booking_crud.py -v -s

# Run a single test
pytest tests/test_booking_crud.py::test_create_booking -v

# Debug with pdb
pytest tests/test_booking_crud.py -v --pdb
```

## API Reference

**Base**: `https://restful-booker.herokuapp.com`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/booking` | Create booking |
| GET | `/booking` | List bookings (with filters) |
| GET | `/booking/{id}` | Get booking by ID |
| PUT | `/booking/{id}` | Update booking |
| DELETE | `/booking/{id}` | Delete booking |

## Dependencies

- **pytest**: Test framework
- **requests**: HTTP client
- **jsonschema**: Schema validation (ready to use)
- **pytest-html**: HTML reporting
- **pytest-xdist**: Parallel execution

## Files Not Included

- `.env` — No secrets; settings hardcoded safe
- `reports/` — Generated at runtime, gitignored
- `__pycache__/` — Python cache, gitignored

## Next Steps

1. **Add Schema Validation** — Validate booking response structure
2. **Auth Support** — Add Bearer token fixtures
3. **Data Generators** — Factory for varied booking payloads
4. **Negative Tests** — Boundary values, SQL injection, type mismatches

## Contact

Questions? Open an issue or reach out to shreya.strategicdesign@gmail.com

---

**Built with**: requests 2.31 | pytest 8.0 | Python 3.11 | GitHub Actions
