import requests
import json

def simple_otp_request():
    phone = input("Enter mobile number (example: 09123456789): ")
    
    # Convert to +98 format
    if phone.startswith('0'):
        phone = '+98' + phone[1:]
    
    url = "https://app.snapp.taxi/api/api-passenger-oauth/v3/mutotp"
    
    payload = {
        "cellphone": phone,
        "attestation": {
            "method": "skip", 
            "platform": "skip"
        },
        "extra_methods": []
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        print(f"Status: {response.status_code}")
        print("Response:", response.json())
    except Exception as e:
        print(f"Error: {e}")

# Run the script
simple_otp_request()