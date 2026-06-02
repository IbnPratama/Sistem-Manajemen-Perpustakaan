import json
import os
import uuid

from library_management.core.algorithms import binary_search, linear_search, merge_sort
from library_management.core.structures import BST, HashTable, LinkedList

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data.json")


def _load():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def _save(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _build_linked_list(books):
    ll = LinkedList()
    for b in books:
        ll.append(b)
    return ll


def _build_hash_table(books):
    ht = HashTable()
    for b in books:
        ht.insert(b["id"], b)
    return ht


def _build_bst(books):
    bst = BST()
    sorted_books = merge_sort(books, lambda x: x["title"].lower())
    for b in sorted_books:
        bst.insert(b["title"].lower(), b)
    return bst


def get_all_books():
    data = _load()
    books = data.get("books", [])
    ll = _build_linked_list(books)
    return ll.to_list()


def add_book(title, author, year, genre, stock):
    data = _load()
    book = {
        "id": str(uuid.uuid4())[:8],
        "title": title,
        "author": author,
        "year": int(year),
        "genre": genre,
        "stock": int(stock),
    }
    ll = _build_linked_list(data["books"])
    ll.append(book)
    data["books"] = ll.to_list()
    _save(data)
    return book


def update_book(book_id, title, author, year, genre, stock):
    data = _load()
    ht = _build_hash_table(data["books"])
    book = ht.get(book_id)
    if book is None:
        return False
    book["title"] = title
    book["author"] = author
    book["year"] = int(year)
    book["genre"] = genre
    book["stock"] = int(stock)
    ht.insert(book_id, book)
    data["books"] = [v for _, v in ht.items()]
    _save(data)
    return True


def delete_book(book_id):
    data = _load()
    ll = _build_linked_list(data["books"])
    removed = ll.remove(lambda b: b["id"] == book_id)
    if removed:
        data["books"] = ll.to_list()
        _save(data)
    return removed


def search_books(query):
    books = get_all_books()
    return linear_search(books, query, lambda b: b["title"] + " " + b["author"])


def get_books_sorted(key="title"):
    books = get_all_books()
    return merge_sort(books, lambda b: str(b.get(key, "")).lower())


def get_book_by_id(book_id):
    data = _load()
    ht = _build_hash_table(data["books"])
    return ht.get(book_id)


def adjust_stock(book_id, delta):
    data = _load()
    ht = _build_hash_table(data["books"])
    book = ht.get(book_id)
    if book is None:
        return False
    book["stock"] = max(0, book["stock"] + delta)
    ht.insert(book_id, book)
    data["books"] = [v for _, v in ht.items()]
    _save(data)
    return True
