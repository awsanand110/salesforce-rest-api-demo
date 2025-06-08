from services.auth_service import SalesforceAuthService
import requests

class SalesforceAPIClient:
    def __init__(self, auth_service: SalesforceAuthService):
        self.auth_service = auth_service
        self.access_token, self.instance_url = self.auth_service.get_access_token()
        self.headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }

    def _refresh_token(self):
        print("Refreshing Salesforce access token...")
        self.access_token, self.instance_url = self.auth_service.get_access_token()

    def request(self, method, endpoint, params=None, json=None):
        if self.headers is None:
            self.headers = {}
        url = f"{self.instance_url}{endpoint}"
        # Add auth and content-type headers
        self.headers.update({
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        })

        response = requests.request(method, url, params=params, json=json, headers=self.headers)

        # If unauthorized, refresh token once and retry
        if response.status_code == 401:
            self._refresh_token()
            self.headers["Authorization"] = f"Bearer {self.access_token}"
            response = requests.request(method, url, params=params, json=json, headers=self.headers)

        return response
