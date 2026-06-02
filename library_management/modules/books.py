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

def create_book(book_id, title, author, category, year):
    if not book_id or not title or not author:
        return False
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            return False
    new_book = {"id": book_id, "title": title, "author": author, "category": category, "year": year}
    data["books"].append(new_book)
    data["logs"].append(f"Added book: {title} (ID: {book_id})")
    save_data(data)
    return True

def read_books():
    return load_data()["books"]

def update_book(book_id, title, author, category, year):
    data = load_data()
    for book in data["books"]:
        if book["id"] == book_id:
            book["title"] = title
            book["author"] = author
            book["category"] = category
            book["year"] = year
            data["logs"].append(f"Updated book ID: {book_id}")
            save_data(data)
            return True
    return False

def delete_book(book_id):
    data = load_data()
    for i, book in enumerate(data["books"]):
        if book["id"] == book_id:
            del data["books"][i]
            data["logs"].append(f"Deleted book ID: {book_id}")
            save_data(data)
            return True
    return False