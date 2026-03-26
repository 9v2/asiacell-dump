# 🎯 Asiacell Application Security Analysis Case Study

This document contains a comprehensive technical breakdown of the `asiacell-4-4-0.apk` (v4.4.0) authentication flow and server responses.

---

## 🔑 Core Infrastructure & Secrets
- **Production Base URL:** `https://odpapp.asiacell.com/`
- **Primary API Key (`X-ODP-API-KEY`):** `1ccbc4c913bc4ce785a0a2de444aa0d6`
- **Encryption:** AES-GCM / AES-CBC for sensitive payload protection.

---

## 🚀 Authentication Flow & Server Responses

### Phase 1: Login Initiation (`/api/v1/login`)
**Request:** `{ "username": "96477XXXXXXXX" }`

| Scenario | HTTP Status | JSON Response Schema |
| :--- | :--- | :--- |
| **Success** | 200 OK | `{"success": true, "nextUrl": "#/...&PID=[TOKEN]", "message": "Waiting for SMS"}` |
| **WAF Block** | 403 Forbidden | `{"success": false}` (Caused by missing DeviceID or invalid TLS fingerprint) |
| **Invalid Num** | 200 OK | `{"success": false, "message": "Invalid phone number format"}` |

### Phase 2: SMS OTP Validation (`/api/v1/smsvalidation`)
**Request:** `{ "username": "...", "pin": "123456", "token": "[PID_FROM_PHASE_1]" }`

| Scenario | HTTP Status | JSON Response Schema |
| :--- | :--- | :--- |
| **Success** | 200 OK | `{"access_token": "JWT_TOKEN", "refresh_token": "REF_TOKEN", "userId": 12345, "success": true}` |
| **Invalid PIN**| 200 OK | `{"success": false, "message": "رمز التأكيد غير صحيح"}` (Invalid PIN) |
| **Expired** | 200 OK | `{"success": false, "message": "Handshake expired"}` |

---

## 🐍 Research Tool: `asiacell_lab.py` (Final)

```python
import requests
import json
import uuid

# Research Configuration
BASE_URL = "https://odpapp.asiacell.com"
API_KEY = "1ccbc4c913bc4ce785a0a2de444aa0d6"

def get_headers():
    """Generates authentic headers to satisfy the F5 WAF."""
    return {
        "X-ODP-API-KEY": API_KEY,
        "DeviceID": str(uuid.uuid4()).replace('-', '')[:16],
        "X-ODP-APP-VERSION": "4.4.0",
        "X-FROM-APP": "odp",
        "X-ODP-CHANNEL": "mobile",
        "X-Device-Type": "[Android][Samsung][SM-G991B][13][HMS]",
        "User-Agent": "okhttp/4.9.1"
    }

def start_login(phone):
    """
    Triggers Stage 1.
    EXPECTED SUCCESS: {"success": True, "nextUrl": "...PID=XXXX", ...}
    """
    url = f"{BASE_URL}/api/v1/login"
    r = requests.post(url, headers=get_headers(), json={"username": phone})
    return r.json()

def verify_otp(phone, pin, token):
    """
    Triggers Stage 2.
    EXPECTED SUCCESS: {"access_token": "...", "success": True, ...}
    EXPECTED FAILURE: {"success": False, "message": "Invalid PIN"}
    """
    url = f"{BASE_URL}/api/v1/smsvalidation"
    payload = {"username": phone, "pin": pin, "token": token}
    r = requests.post(url, headers=get_headers(), json=payload)
    return r.json()
```

---

## 🕵️‍♂️ Advanced Research Notes
- **WAF Evasion:** The `DeviceID` must be a valid UUID. The `X-Device-Type` must follow the `[Android][...][...][...][...]` pattern.
- **Session Security:** After Phase 2, all further API calls (like `/api/v1/profile/view`) require the `Authorization: Bearer <access_token>` header.
- **Data Leaks:** The `/api/v1/login-screen` endpoint can be accessed without a token using just the `X-ODP-API-KEY`.
