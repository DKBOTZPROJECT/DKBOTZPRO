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
    
    def validate_params(self, **kwargs):
        missing_params = [key for key, value in kwargs.items() if value is None or value == ""]
        if missing_params:
            return False, f"Missing parameters: {', '.join(missing_params)}"
        return True, None
    
    def handle_exception(self, e):
        return False, f"An error occurred: {str(e)}"
    
    try:
        def premium_login(self, username=None, password=None):
            is_valid, error = self.validate_params(username=username, password=password)
            if not is_valid:
                return False, error
            
            params = {"username": username, "password": password}
            response = requests.get(PREMIUM_LOGIN_API, params=params)
            return True, response.json()
    except Exception as e:
        handle_exception(e)
    
    try:
        def premium_verify_product(self, username=None, password=None, product=None):
            is_valid, error = self.validate_params(username=username, password=password, product=product)
            if not is_valid:
                return False, error
            
            params = {"username": username, "password": password, "product": product}
            response = requests.get(PREMIUM_PRODUCT_VERIFY_API, params=params)
            return True, response.json()
    except Exception as e:
        handle_exception(e)
    
    try:
        def premium_edit_server(self, username=None, password=None, product=None, servername=None, server_num=None, value=None):
            is_valid, error = self.validate_params(username=username, password=password, product=product, servername=servername, server_num=server_num, value=value)
            if not is_valid:
                return False, error
            
            params = {"username": username, "password": password, "product": product, "servername": servername, "server_num": server_num, "value": value}
            response = requests.get(PREMIUM_SERVER_API, params=params)
            return True, response.json()
    except Exception as e:
        handle_exception(e)
    
    try:
        def convert(self, upi_id=None, payee_name=None, amount=None):
            is_valid, error = self.validate_params(upi_id=upi_id, payee_name=payee_name, amount=amount)
            if not is_valid:
                return False, error
            
            url = QR_LINK
            params = {'text': f'upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR'}
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                return (True, data.get('qr_link')) if data.get('status') else (False, "Failed to generate QR code.")
            else:
                return False, f"Error: Received status code {response.status_code}."
    except Exception as e:
        handle_exception(e)
    
    try:
        def encode(self, text=None):
            if not text:
                return False, "Missing text to encode"
            return True, base64.b64encode(text.encode('utf-8')).decode('utf-8')
    except Exception as e:
        handle_exception(e)
    
    try:
        def decode(self, encoded_text=None):
            if not encoded_text:
                return False, "Missing text to decode"
            return True, base64.b64decode(encoded_text.encode('utf-8')).decode('utf-8')
    except Exception as e:
        handle_exception(e)
