import os
import requests
from dotenv import load_dotenv

load_dotenv()

HMS_API_KEY = os.getenv("HMS_ACCESS_KEY")
HMS_API_SECRET = os.getenv("HMS_SECRET")
HMS_TOKEN = os.getenv("HMS_TOKEN")
HMS_TEMPLATE_ID = os.getenv("HMS_TEMPLATE_ID")
HMS_API_URL = "https://api.100ms.live/v2"

def get_auth_headers():
    return {
        "Authorization": f"Bearer {HMS_TOKEN}",
        "Content-Type": "application/json"
    }

def create_room(name, description=""):
    url = f"{HMS_API_URL}/rooms"
    data = {
        "name": name,
        "description": description,
        "template_id": HMS_TEMPLATE_ID
    }
    response = requests.post(url, json=data, headers=get_auth_headers())
    response.raise_for_status()
    return response.json()["id"]

def generate_code_for_role(room_id,role):
    url = f"{HMS_API_URL}/room-codes/room/{room_id}/role/{role}"

    response = requests.post(url, headers=get_auth_headers())
    response.raise_for_status()
    return response.json()["code"]

def generate_link_for_role(room_id,role):
    id = generate_code_for_role(room_id,role)
    return f"https://webdoctor.app.100ms.live/meeting/{id}"


def disable_room(room_id):
    url = f"{HMS_API_URL}/rooms/{room_id}"
    data = {
        "enabled": False
    }
    response = requests.post(url, json=data, headers=get_auth_headers())
    response.raise_for_status()
    return response.json()["enabled"]


