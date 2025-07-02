import requests

EXPO_PUSH_URL = "https://exp.host/--/api/v2/push/send"

def send_expo_push(token, title, body, data=None):
    if not token:
        return False
    payload = {
        "to": token,
        "sound": "default",
        "title": title,
        "body": body,
        "data": data or {},
    }
    headers = {"Content-Type": "application/json"}
    try:
        response = requests.post(EXPO_PUSH_URL, json=payload, headers=headers, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"[ExpoPush] Error: {e}")
        return False
