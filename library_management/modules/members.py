from modules.books import load_raw_data, save_raw_data
from core.structures import LinkedList, BinarySearchTree

class MemberManager:
    def __init__(self):
        self.members_list = LinkedList()
        self.members_bst = BinarySearchTree()
        self.reload_data()

    def reload_data(self):
        data = load_raw_data()
        raw_members = data.get("members", [])
        self.members_list.from_list(raw_members)
        self.members_bst = BinarySearchTree()
        for member in raw_members:
            self.members_bst.insert(member["id"], member)

    def get_all_members(self):
        return self.members_list.to_list()

    def create_member(self, member_id, name, email):
        if self.members_bst.search(member_id) is not None:
            return False, f"Anggota dengan ID {member_id} sudah terdaftar!"

        new_member = {
            "id": member_id,
            "name": name,
            "email": email,
            "active_borrowings": 0  
        }

        data = load_raw_data()
        data["members"].append(new_member)
        save_raw_data(data)

        self.reload_data()
        return True, "Anggota berhasil didaftarkan!"

    def read_member_by_id(self, member_id):
        return self.members_bst.search(member_id)

    def update_member(self, member_id, name, email):
        data = load_raw_data()
        found = False
        
        for member in data["members"]:
            if member["id"] == member_id:
                member["name"] = name
                member["email"] = email
                found = True
                break
                
        if not found:
            return False, "Anggota tidak ditemukan!"
            
        save_raw_data(data)
        self.reload_data()
        return True, "Data anggota berhasil diperbarui!"

    def delete_member(self, member_id):
        current_member = self.read_member_by_id(member_id)
        if current_member and current_member.get("active_borrowings", 0) > 0:
            return False, "Gagal! Anggota masih memiliki pinjaman buku yang belum kembali."

        data = load_raw_data()
        original_count = len(data["members"])
        data["members"] = [m for m in data["members"] if m["id"] != member_id]
        
        if len(data["members"]) == original_count:
            return False, "Anggota tidak ditemukan!"
            
        save_raw_data(data)
        self.reload_data()
        return True, "Data Anggota berhasil dihapus!"