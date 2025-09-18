import requests
import json

def divar_auth(phone):
    """
    Send verification code to phone number using Divar API
    
    Args:
        phone (str): Phone number (with or without country code)
    
    Returns:
        bool: True if code was sent successfully, False otherwise
    """
    # Normalize phone number (remove +98 if present and ensure it starts with 0)
    if phone.startswith('+98'):
        phone = '0' + phone[3:]
    elif phone.startswith('98'):
        phone = '0' + phone[2:]
    
    # API endpoint and headers
    url = "https://api.divar.ir/v5/auth/authenticate"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    
    # Request payload
    payload = {"phone": phone}
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response_data = response.json()
        
        # Check if code was sent successfully
        if response_data.get("authenticate_response") == "AUTHENTICATION_VERIFICATION_CODE_SENT":
            print(f"(Divar) Code was sent to {phone}")
            return True
        else:
            print(f"(Divar) Failed to send code: {response_data}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"(Divar) Request error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"(Divar) JSON decode error: {e}")
        return False

# Example usage
if __name__ == "__main__":
    # Get phone number from user
    phone_number = input("Enter phone number (e.g., 09123456789 or +989123456789): ").strip()
    
    # Send verification code
    if divar_auth(phone_number):
        print("Verification code sent successfully!")
    else:
        print("Failed to send verification code.")