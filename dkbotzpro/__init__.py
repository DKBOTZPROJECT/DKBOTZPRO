import requests
import base64
from .links import *
class DKBotzPro:
    def __init__(self, service):
        self.service = service

    def convert(self, upi_id, payee_name, amount):
        """
        Generates a QR code link for a UPI payment request.
        Returns a tuple: (True, qr_link) on success, (False, error_message) on failure.
        """
        if self.service == "upi_qr":
            url = QR_LINK
            params = {
                'text': f'upi://pay?pa={upi_id}&pn={payee_name}&am={amount}&cu=INR'
            }
            
            try:
                response = requests.get(url, params=params)
                # Check if the request was successful
                if response.status_code == 200:
                    data = response.json()
                    if data.get('status'):
                        return True, data.get('qr_link')  # Return True and the QR link
                    else:
                        return False, "Failed to generate QR code. API response status is false."
                else:
                    return False, f"Error: Received status code {response.status_code} from the server."
            except requests.exceptions.RequestException as e:
                return False, f"An error occurred during the request: {e}"
            except Exception as e:
                return False, f"An unexpected error occurred: {e}"

        return False, "Invalid service selected. Choose 'upi_qr' for UPI QR generation."

    def encode(self, text):
        """
        Encodes the given text into Base64.
        """
        if self.service == "base64":
            byte_data = text.encode('utf-8')
            encoded_data = base64.b64encode(byte_data)
            return encoded_data.decode('utf-8')
        else:
            return "Invalid service for Base64 operations."

    def decode(self, encoded_text):
        """
        Decodes the given Base64 text back to the original string.
        """
        if self.service == "base64":
            byte_data = encoded_text.encode('utf-8')
            decoded_data = base64.b64decode(byte_data)
            return decoded_data.decode('utf-8')
        else:
            return "Invalid service for Base64 operations."


