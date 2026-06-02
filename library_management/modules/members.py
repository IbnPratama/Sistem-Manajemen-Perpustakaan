import json
import os

DATA_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")

def load_data():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"books": [], "members": [], "transactions": [], "reservations": [], "logs": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def create_member(member_id, name, email):
    if not member_id or not name:
        return False
    data = load_data()
    for m in data["members"]:
        if m["id"] == member_id:
            return False
    new_member = {"id": member_id, "name": name, "email": email}
    data["members"].append(new_member)
    data["logs"].append(f"Registered member: {name} (ID: {member_id})")
    save_data(data)
    return True

def read_members():
    return load_data()["members"]

def update_member(member_id, name, email):
    data = load_data()
    for m in data["members"]:
        if m["id"] == member_id:
            m["name"] = name
            m["email"] = email
            data["logs"].append(f"Updated member ID: {member_id}")
            save_data(data)
            return True
    return False

def delete_member(member_id):
    data = load_data()
    for i, m in enumerate(data["members"]):
        if m["id"] == member_id:
            del data["members"][i]
            data["logs"].append(f"Removed member ID: {member_id}")
            save_data(data)
            return True
    return False