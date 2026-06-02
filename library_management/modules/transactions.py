import json
import os
import uuid
from datetime import datetime

from library_management.core.algorithms import linear_search, merge_sort
from library_management.core.structures import HashTable, LinkedList, Queue, Stack
from library_management.modules import books as book_module
from library_management.modules import members as member_module

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data.json")


def _load():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def _save(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _build_hash_table(transactions):
    ht = HashTable()
    for t in transactions:
        ht.insert(t["id"], t)
    return ht


def _build_linked_list(transactions):
    ll = LinkedList()
    for t in transactions:
        ll.append(t)
    return ll


def get_all_transactions():
    data = _load()
    ll = _build_linked_list(data.get("transactions", []))
    return ll.to_list()


def get_active_loans():
    transactions = get_all_transactions()
    return [t for t in transactions if t["status"] == "dipinjam"]


def get_return_queue():
    active = get_active_loans()
    q = Queue()
    for t in active:
        q.enqueue(t)
    return q


def get_history_stack():
    transactions = get_all_transactions()
    sorted_t = merge_sort(transactions, lambda t: t["borrow_date"])
    stack = Stack()
    for t in sorted_t:
        stack.push(t)
    return stack


def borrow_book(member_id, book_id):
    book = book_module.get_book_by_id(book_id)
    if book is None:
        return False, "Buku tidak ditemukan"
    if book["stock"] <= 0:
        return False, "Stok buku habis"
    member = member_module.get_member_by_id(member_id)
    if member is None:
        return False, "Anggota tidak ditemukan"
    if member.get("active_loans", 0) >= 3:
        return False, "Anggota sudah meminjam maksimum 3 buku"

    data = _load()
    transaction = {
        "id": str(uuid.uuid4())[:8],
        "member_id": member_id,
        "member_name": member["name"],
        "book_id": book_id,
        "book_title": book["title"],
        "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "return_date": None,
        "status": "dipinjam",
    }
    ll = _build_linked_list(data["transactions"])
    ll.append(transaction)
    data["transactions"] = ll.to_list()
    _save(data)

    book_module.adjust_stock(book_id, -1)
    member_module.update_active_loans(member_id, 1)
    return True, "Peminjaman berhasil"


def return_book(transaction_id):
    data = _load()
    ht = _build_hash_table(data["transactions"])
    transaction = ht.get(transaction_id)
    if transaction is None:
        return False, "Transaksi tidak ditemukan"
    if transaction["status"] == "dikembalikan":
        return False, "Buku sudah dikembalikan"

    transaction["status"] = "dikembalikan"
    transaction["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    ht.insert(transaction_id, transaction)
    data["transactions"] = [v for _, v in ht.items()]
    _save(data)

    book_module.adjust_stock(transaction["book_id"], 1)
    member_module.update_active_loans(transaction["member_id"], -1)
    return True, "Pengembalian berhasil"


def delete_transaction(transaction_id):
    data = _load()
    ll = _build_linked_list(data["transactions"])
    removed = ll.remove(lambda t: t["id"] == transaction_id)
    if removed:
        data["transactions"] = ll.to_list()
        _save(data)
        return True
    return False


def search_transactions(query):
    transactions = get_all_transactions()
    return linear_search(transactions, query, lambda t: t["member_name"] + " " + t["book_title"])


def get_transactions_sorted(key="borrow_date"):
    transactions = get_all_transactions()
    return merge_sort(transactions, lambda t: str(t.get(key, "")))
