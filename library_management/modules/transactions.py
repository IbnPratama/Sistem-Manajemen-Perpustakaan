import json
import os
from datetime import datetime

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

def borrow_book(book_id, member_id):
    data = load_data()
    book_exists = any(b["id"] == book_id for b in data["books"])
    member_exists = any(m["id"] == member_id for m in data["members"])
    if not book_exists or not member_exists:
        return False, "Book ID or Member ID not found."
    for t in data["transactions"]:
        if t["book_id"] == book_id and t["status"] == "Borrowed":
            return False, "Book is currently borrowed by someone else."
    new_tx = {
        "tx_id": str(len(data["transactions"]) + 1),
        "book_id": book_id,
        "member_id": member_id,
        "borrow_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "Borrowed"
    }
    data["transactions"].append(new_tx)
    data["logs"].append(f"Book {book_id} borrowed by Member {member_id}")
    save_data(data)
    return True, "Success"

def return_book(book_id):
    data = load_data()
    for t in data["transactions"]:
        if t["book_id"] == book_id and t["status"] == "Borrowed":
            t["status"] = "Returned"
            data["logs"].append(f"Book {book_id} returned to shelf")
            next_res_idx = -1
            for i, r in enumerate(data["reservations"]):
                if r["book_id"] == book_id:
                    next_res_idx = i
                    break
            if next_res_idx != -1:
                next_res = data["reservations"].pop(next_res_idx)
                new_tx = {
                    "tx_id": str(len(data["transactions"]) + 1),
                    "book_id": book_id,
                    "member_id": next_res["member_id"],
                    "borrow_date": datetime.now().strftime("%Y-%m-%d"),
                    "status": "Borrowed"
                }
                data["transactions"].append(new_tx)
                data["logs"].append(f"Reservation fulfilled automatically: Book {book_id} assigned to Member {next_res['member_id']}")
            save_data(data)
            return True, "Success"
    return False, "No active borrowing record found for this book."

def add_reservation(book_id, member_id):
    data = load_data()
    book_exists = any(b["id"] == book_id for b in data["books"])
    member_exists = any(m["id"] == member_id for m in data["members"])
    if not book_exists or not member_exists:
        return False
    new_res = {"book_id": book_id, "member_id": member_id}
    data["reservations"].append(new_res)
    data["logs"].append(f"Reservation queue added for Book {book_id} by Member {member_id}")
    save_data(data)
    return True