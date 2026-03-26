import requests
import json

# Discovered from Reverse Engineering
BASE_URL = "https://odpapp.asiacell.com"
API_KEY = "1ccbc4c913bc4ce785a0a2de444aa0d6"

def probe_sensitive_info(token):
    headers = {
        "X-ODP-API-KEY": API_KEY,
        "Authorization": f"Bearer {token}",
        "X-FROM-APP": "odp",
        "X-ODP-CHANNEL": "mobile"
    }
    
    endpoints = [
        "/api/v1/profile/view",
        "/api/v1/profile/subscriptions",
        "/api/v1/notifications"
    ]
    
    for ep in endpoints:
        print(f"[*] Probing {ep} with your token...")
        r = requests.get(f"{BASE_URL}{ep}", headers=headers)
        print(f"[+] Result ({r.status_code}):")
        try:
            print(json.dumps(r.json(), indent=2))
        except:
            print(r.text)
        print("-" * 30)

if __name__ == "__main__":
    print("--- ASIACELL SECURITY EXPLORER ---")
    # user_token = input("Paste the token caught by Frida: ")
    # probe_sensitive_info(user_token)
