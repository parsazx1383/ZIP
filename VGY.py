import requests
import json

def digikala_auth(phone):
    """
    Send authentication request to Digikala API
    
    Args:
        phone (str): Phone number (with or without country code)
    
    Returns:
        bool: True if request was successful, False otherwise
    """
    # Normalize phone number
    if phone.startswith('+98'):
        phone = '0' + phone[3:]
    elif phone.startswith('98'):
        phone = '0' + phone[2:]
    
    # API endpoint and headers
    url = "https://api.digikala.com/v1/user/authenticate/"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_10 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }
    
    # Request payload
    payload = {
        "backUrl": "/profile/",
        "username": phone,
        "otp_call": False,
        "hash": None
    }
    
    try:
        # Send POST request
        response = requests.post(url, headers=headers, json=payload, timeout=10)
        response_data = response.json()
        
        # Check if request was successful
        if response_data.get("status") == 200:
            data = response_data.get("data", {})
            print(f"(Digikala) Success - Phone: {data.get('phone')}")
            print(f"(Digikala) Has Account: {data.get('has_account')}")
            print(f"(Digikala) Login Method: {data.get('login_method')}")
            print(f"(Digikala) Has Password: {data.get('has_password')}")
            return True
        else:
            print(f"(Digikala) Failed: {response_data}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"(Digikala) Request error: {e}")
        return False
    except json.JSONDecodeError as e:
        print(f"(Digikala) JSON decode error: {e}")
        return False

# Combined function for both services
def send_verification_services(phone):
    """
    Send verification to both Torob and Digikala services
    
    Args:
        phone (str): Phone number
    """
    # Your existing Torob function (modified to match the style)
    def torob(phone):
        phone = '0' + phone.split('+98')[1] if '+98' in phone else phone
        torobH = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'cookie': 'abtest=next_pwa; search_session=ofwjiyqqethomevqrgzxvopjtgkgimdc; _gcl_au=1.1.805505755.1639260830; _gid=GA1.2.683761449.1639260830; _gat_UA-105982196-1=1; _ga_CF4KGKM3PG=GS1.1.1639260830.1.0.1639260830.0; _clck=130ifw1|1|ex6|0; _ga=GA1.2.30224238.1639260830',
            'origin': 'https://torob.com',
            'referer': 'https://torob.com/',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
        }
        try:
            torobR = requests.get(f"https://api.torob.com/a/phone/send-pin/?phone_number={phone}", headers=torobH, timeout=5).json()
            if torobR.get("message") == "pin code sent":
                print(f'(Torob) Code Was Sent to {phone}')
                return True
        except:
            print("(Torob) Failed to send code")
            return False
    
    # Call both services
    torob_result = torob(phone)
    digikala_result = digikala_auth(phone)
    
    return torob_result, digikala_result

# Example usage
if __name__ == "__main__":
    # Get phone number from user
    phone_number = input("Enter phone number (e.g., 09123456789 or +989123456789): ").strip()
    
    print("Sending requests to services...")
    print("-" * 40)
    
    # Send to both services
    torob_success, digikala_success = send_verification_services(phone_number)
    
    print("-" * 40)
    print(f"Results: Torob: {'✓' if torob_success else '✗'}, Digikala: {'✓' if digikala_success else '✗'}")