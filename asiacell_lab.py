import requests
import json
import uuid

# Research Configuration
BASE_URL = "https://odpapp.asiacell.com"
API_KEY = "1ccbc4c913bc4ce785a0a2de444aa0d6"

def get_headers(token=None):
    """Generates authentic headers including the dynamic Bearer token."""
    headers = {
        "X-ODP-API-KEY": API_KEY,
        "DeviceID": str(uuid.uuid4()).replace('-', '')[:16],
        "X-ODP-APP-VERSION": "4.4.0",
        "X-FROM-APP": "odp",
        "X-ODP-CHANNEL": "mobile",
        "X-Device-Type": "[Android][Samsung][SM-G991B][13][HMS]",
        "User-Agent": "okhttp/4.9.1",
        "Content-Type": "application/json"
    }
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers

def get_profile_details(token):
    """
    Fetches the full PII profile of the current user.
    FIELDS EXPOSED: firstName, lastName, thirdName, phone, email, photoURL
    """
    url = f"{BASE_URL}/api/v1/profile/view"
    print(f"[*] Extracting PII from {url}...")
    r = requests.get(url, headers=get_headers(token))
    
    if r.status_code == 200:
        data = r.json().get("data", {})
        print(f"[!] SUCCESS: PII Extracted for {data.get('firstName')} {data.get('lastName')}")
        return data
    return None

def get_subscriptions(token):
    """
    Lists all active voice and data plans.
    FIELDS EXPOSED: title, validity, actionButton status
    """
    url = f"{BASE_URL}/api/v1/profile/subscriptions"
    r = requests.get(url, headers=get_headers(token))
    return r.json()

# Full Auth Flow Template:
# 1. start_login(phone) -> Get PID
# 2. verify_otp(phone, otp, PID) -> Get Bearer Token
# 3. get_profile_details(Bearer) -> Extract Private Data
