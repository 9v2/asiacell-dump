# 🛡️ Asiacell Security Audit & API Dossier (v4.4.0)

## 1. 🔑 Security Gatekeepers
| Component | Value / Implementation |
| :--- | :--- |
| **Main API Key** | `1ccbc4c913bc4ce785a0a2de444aa0d6` |
| **Request Signing** | Header-based authentication using dynamic Bearer tokens. |
| **WAF Protection** | F5 BIG-IP (Application Security Manager). |
| **Device ID** | UUID v4 (Persistent across installs). |

## 2. 🚀 The Authentication Handshake
1. **Trigger:** `/api/v1/login` (POST) - Returns a **PID** (Process ID).
2. **Verify:** `/api/v1/smsvalidation` (POST) - Uses PID + OTP to return a **JWT Access Token**.

## 3. 🎯 High-Value Targets (Potential IDOR)
The following endpoints handle sensitive user data and should be tested for authorization bypass:
- `/api/v1/profile/view`: Returns full user PII.
- `/api/v1/profile/subscriptions`: Returns active data/voice plan details.
- `/api/v1/cdr/detail`: Call Detail Records (Logs of every call/SMS).

## 🕵️‍♂️ Research Guide: How to bypass WAF & Intercept
1. **Tool:** Use `mitmweb --mode transparent`.
2. **Evasion:** Inject the `custom_bypass.js` Frida script to disable SSL Pinning.
3. **Identity:** Use the Python `asiacell_lab.py` script to simulate an authorized Android device.
