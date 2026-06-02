import json
import os
from core.structures import LinkedList, BinarySearchTree, HashMap

DATA_FILE = "data.json"

def load_raw_data():
    if not os.path.exists(DATA_FILE):
        initial_data = {"books": [], "members": [], "transactions": [], "graph_edges": []}
        with open(DATA_FILE, 'sig') as f:
            json.dump(initial_data, f, indent=4)
        return initial_data
    
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {"books": [], "members": [], "transactions": [], "graph_edges": []}

def save_raw_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

class BookManager:
    def __init__(self):
        self.books_list = LinkedList()
        self.books_bst = BinarySearchTree()
        self.books_hashmap = HashMap(size=10)
        self.reload_data()

    def reload_data(self):
        data = load_raw_data()
        raw_books = data.get("books", [])
        self.books_list.from_list(raw_books)
        self.books_bst = BinarySearchTree()
        self.books_hashmap = HashMap(size=10)
        genre_groups = {}

        for book in raw_books:
            self.books_bst.insert(book["id"], book)
            genre = book.get("genre", "Umum")
            if genre not in genre_groups:
                genre_groups[genre] = []
            genre_groups[genre].append(book)
        for genre, books in genre_groups.items():
            self.books_hashmap.put(genre, books)

    def get_all_books(self):
        return self.books_list.to_list()

    def create_book(self, book_id, title, author, genre):
        if self.books_bst.search(book_id) is not None:
            return False, f"Buku dengan ID {book_id} sudah terdaftar!"

        new_book = {
            "id": book_id,
            "title": title,
            "author": author,
            "genre": genre,
            "status": "Tersedia"
        }
        data = load_raw_data()
        data["books"].append(new_book)
        save_raw_data(data)

        self.reload_data()
        return True, "Buku berhasil ditambahkan!"

    def read_book_by_id(self, book_id):
        return self.books_bst.search(book_id)

    def get_books_by_genre(self, genre):
        books = self.books_hashmap.get(genre)
        return books if books else []

    def update_book(self, book_id, title, author, genre, status):
        data = load_raw_data()
        found = False
        
        for book in data["books"]:
            if book["id"] == book_id:
                book["title"] = title
                book["author"] = author
                book["genre"] = genre
                book["status"] = status
                found = True
                break
        
        if not found:
            return False, "Buku tidak ditemukan!"
        
        save_raw_data(data)
        self.reload_data()
        return True, "Data buku berhasil diperbarui!"

    def delete_book(self, book_id):
        data = load_raw_data()
        original_count = len(data["books"])
        data["books"] = [b for b in data["books"] if b["id"] != book_id]
        
        if len(data["books"]) == original_count:
            return False, "Buku gagal dihapus atau tidak ditemukan!"
            
        save_raw_data(data)
        self.reload_data()
        return True, "Buku berhasil dihapus!"