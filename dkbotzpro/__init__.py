import requests
import base64
from .api import *




class DKBotzPro:
    """Handles different services dynamically."""

    def __init__(self, service):
        self.service = service

        if service == "premium":
            self.login = self.premium_login
            self.verify_product = self.premium_verify_product
            self.edit_server = self.premium_edit_server
        elif service == "upi_qr":
            self.execute = self.convert  # Allow only convert
        elif service == "base64":
            self.encode_text = self.encode
            self.decode_text = self.decode
        else:
            raise ValueError("Invalid service type! Choose 'premium', 'upi_qr', or 'base64'.")
            
    def premium_login(self, username, password):
        params = {"username": username, "password": password}
        try:
            response = requests.get(PREMIUM_LOGIN_API, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"An error occurred: {e}"}
            
    def premium_verify_product(self, username, password, product):
        params = {"username": username, "password": password, "product": product}
        try:
            response = requests.get(PREMIUM_PRODUCT_VERIFY_API, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"An error occurred: {e}"}
            
    def premium_edit_server(self, username, password, servername, server_num, value):
        params = {"username": username, "password": password, "product": product, "servername": servername, "server_num": server_num, "value": value}
        try:
            response = requests.get(PREMIUM_PRODUCT_VERIFY_API, params=params)
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"status": False, "message": f"An error occurred: {e}"}
            
    def convert(self, upi_id, payee_name, amount):
        url = QR_LINK
        params = {'text': f'upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR'}
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return (True, data.get('qr_link')) if data.get('status') else (False, "Failed to generate QR code.")
            else:
                return False, f"Error: Received status code {response.status_code}."
        except requests.exceptions.RequestException as e:
            return False, f"An error occurred: {e}"

    def encode(self, text):
        return base64.b64encode(text.encode('utf-8')).decode('utf-8')

    def decode(self, encoded_text):
        return base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')






