import requests
from dotenv import load_dotenv
import os

load_dotenv()

class SalesforceAuthService:
    def __init__(self):
        self.client_id = os.getenv("SALESFORCE_CLIENT_ID")
        self.client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")
        self.username = os.getenv("SALESFORCE_USERNAME")
        self.password = os.getenv("SALESFORCE_PASSWORD")
        self.security_token = os.getenv("SALESFORCE_SECURITY_TOKEN")
        self.token_url = f'{os.getenv("SALESFORCE_LOGIN_URL")}/services/oauth2/token'


    def get_access_token(self):
        final_password = self.password + self.security_token
        payload = {
            "grant_type": "password",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "username": self.username,
            "password": final_password
        }

        print(payload)
        print(self.token_url)

        response = requests.post(self.token_url, data=payload)

        if response.status_code == 200:
            token_data = response.json()
            return  token_data["access_token"],token_data["instance_url"]
        else:
            raise Exception(f"Salesforce Auth failed: {response.status_code} {response.text}")


sf = SalesforceAuthService()
access_token,instance_url = sf.get_access_token()

print(f"Access Token: {access_token}\nInstance URL: {instance_url}")