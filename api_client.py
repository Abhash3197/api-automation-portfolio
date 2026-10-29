import requests
from config.settings import BASE_URL, TIMEOUT


class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.timeout = TIMEOUT
        self.session = requests.Session()
        self.token = None

    def get_auth_token(self):
        """Get auth token for protected operations"""
        if not self.token:
            response = self.session.post(
                f"{self.base_url}/auth",
                json={"username": "admin", "password": "password123"},
                timeout=self.timeout
            )
            if response.status_code == 200:
                self.token = response.json().get("token")
        return self.token

    def get(self, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.get(url, timeout=self.timeout, **kwargs)

    def post(self, endpoint: str, data: dict = None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        return self.session.post(url, json=data, timeout=self.timeout, **kwargs)

    def put(self, endpoint: str, data: dict = None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get("headers", {})
        headers["Cookie"] = f"token={self.get_auth_token()}"
        kwargs["headers"] = headers
        return self.session.put(url, json=data, timeout=self.timeout, **kwargs)

    def patch(self, endpoint: str, data: dict = None, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get("headers", {})
        headers["Cookie"] = f"token={self.get_auth_token()}"
        kwargs["headers"] = headers
        return self.session.patch(url, json=data, timeout=self.timeout, **kwargs)

    def delete(self, endpoint: str, **kwargs):
        url = f"{self.base_url}{endpoint}"
        headers = kwargs.get("headers", {})
        headers["Cookie"] = f"token={self.get_auth_token()}"
        kwargs["headers"] = headers
        return self.session.delete(url, timeout=self.timeout, **kwargs)

    def close(self):
        self.session.close()
