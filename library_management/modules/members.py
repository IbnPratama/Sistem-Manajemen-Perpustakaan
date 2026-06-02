import json
import os
import uuid

from library_management.core.algorithms import linear_search, merge_sort
from library_management.core.structures import HashTable, LinkedList

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data.json")


def _load():
    with open(DATA_PATH, "r") as f:
        return json.load(f)


def _save(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=2)


def _build_linked_list(members):
    ll = LinkedList()
    for m in members:
        ll.append(m)
    return ll


def _build_hash_table(members):
    ht = HashTable()
    for m in members:
        ht.insert(m["id"], m)
    return ht


def get_all_members():
    data = _load()
    ll = _build_linked_list(data.get("members", []))
    return ll.to_list()


def add_member(name, email, phone):
    data = _load()
    member = {"id": str(uuid.uuid4())[:8], "name": name, "email": email, "phone": phone, "active_loans": 0}
    ll = _build_linked_list(data["members"])
    ll.append(member)
    data["members"] = ll.to_list()
    _save(data)
    return member


def update_member(member_id, name, email, phone):
    data = _load()
    ht = _build_hash_table(data["members"])
    member = ht.get(member_id)
    if member is None:
        return False
    member["name"] = name
    member["email"] = email
    member["phone"] = phone
    ht.insert(member_id, member)
    data["members"] = [v for _, v in ht.items()]
    _save(data)
    return True


def delete_member(member_id):
    data = _load()
    ht = _build_hash_table(data["members"])
    member = ht.get(member_id)
    if member and member.get("active_loans", 0) > 0:
        return False, "Anggota masih memiliki pinjaman aktif"
    ll = _build_linked_list(data["members"])
    removed = ll.remove(lambda m: m["id"] == member_id)
    if removed:
        data["members"] = ll.to_list()
        _save(data)
        return True, "Berhasil dihapus"
    return False, "Anggota tidak ditemukan"


def search_members(query):
    members = get_all_members()
    return linear_search(members, query, lambda m: m["name"] + " " + m["email"])


def get_members_sorted():
    members = get_all_members()
    return merge_sort(members, lambda m: m["name"].lower())


def get_member_by_id(member_id):
    data = _load()
    ht = _build_hash_table(data["members"])
    return ht.get(member_id)


def update_active_loans(member_id, delta):
    data = _load()
    ht = _build_hash_table(data["members"])
    member = ht.get(member_id)
    if member is None:
        return False
    member["active_loans"] = max(0, member.get("active_loans", 0) + delta)
    ht.insert(member_id, member)
    data["members"] = [v for _, v in ht.items()]
    _save(data)
    return True
