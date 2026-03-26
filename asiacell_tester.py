import requests
import json
import uuid

class AsiacellProfessionalTester:
    BASE_URL = "https://odpapp.asiacell.com"
    API_KEY = "1ccbc4c913bc4ce785a0a2de444aa0d6"
    
    def __init__(self):
        self.device_id = str(uuid.uuid4())
        self.device_type = "[Android][Samsung][SM-G991B][13][HMS]"
        self.headers = {
            "X-ODP-API-KEY": self.API_KEY,
            "DeviceID": self.device_id,
            "X-Device-Type": self.device_type,
            "X-OS-Version": "13",
            "X-ODP-APP-VERSION": "4.4.0",
            "X-FROM-APP": "odp",
            "X-ODP-CHANNEL": "mobile",
            "User-Agent": "okhttp/4.9.1",
            "Content-Type": "application/json"
        }

    def validate_sms(self, phone, pin, token):
        """Probes the /api/v1/smsvalidation endpoint"""
        url = f"{self.BASE_URL}/api/v1/smsvalidation"
        payload = {
            "username": phone,
            "pin": pin,
            "token": token
        }
        
        print(f"[*] Validating SMS OTP for {phone}...")
        print(f"[*] Token (PID): {token}")
        
        try:
            r = requests.post(url, headers=self.headers, json=payload, timeout=15)
            print(f"[+] Status: {r.status_code}")
            print("\n[+] JSON Response:")
            print(json.dumps(r.json(), indent=2))
        except Exception as e:
            print(f"[!] Error: {str(e)}")

if __name__ == "__main__":
    tester = AsiacellProfessionalTester()
    print("--- ASIACELL STAGE 2 PROBE ---")
    
    # Using the PID we just caught from your previous run
    test_phone = "9647700000000"
    test_pin = "123456" # Fake PIN
    test_token = "24e68bea-1d92-42fe-b43f-450499ebc389"
    
    tester.validate_sms(test_phone, test_pin, test_token)
