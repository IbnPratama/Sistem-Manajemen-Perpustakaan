from datetime import datetime
from modules.books import load_raw_data, save_raw_data
from core.structures import Stack, Queue, Graph

class TransactionManager:
    def __init__(self):
        self.undo_stack = Stack()          
        self.reservation_queue = Queue()   
        self.relation_graph = Graph()      
        self.reload_data()

    def reload_data(self):
        data = load_raw_data()
        self.relation_graph = Graph()
        edges = data.get("graph_edges", [])
        for edge in edges:
            self.relation_graph.add_relation_edge(edge[0], edge[1])

    def get_all_transactions(self):
        data = load_raw_data()
        return data.get("transactions", [])

    def borrow_book(self, member_id, book_id):
        """Logika Transaksi Peminjaman Buku"""
        data = load_raw_data()
        book_target = next((b for b in data["books"] if b["id"] == book_id), None)
        member_target = next((m for m in data["members"] if m["id"] == member_id), None)

        if not book_target:
            return False, "ID Buku tidak valid!"
        if not member_target:
            return False, "ID Anggota tidak valid!"
        if book_target["status"] == "Dipinjam":
            self.reservation_queue.enqueue({"member_id": member_id, "book_id": book_id})
            return True, "Buku sedang dipinjam. Anda dimasukkan ke dalam Antrean Reservasi Buku."

        book_target["status"] = "Dipinjam"
        member_target["active_borrowings"] += 1

        new_tx = {
            "tx_id": f"TX-{int(datetime.now().timestamp())}",
            "member_id": member_id,
            "member_name": member_target["name"],
            "book_id": book_id,
            "book_title": book_target["title"],
            "borrow_date": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "return_date": None
        }
        member_past_tx = [t for t in data["transactions"] if t["member_id"] == member_id and t["return_date"] is None]
        for past_tx in member_past_tx:
            edge = [past_tx["book_id"], book_id]
            if edge not in data["graph_edges"] and [book_id, past_tx["book_id"]] not in data["graph_edges"]:
                data["graph_edges"].append(edge)

        data["transactions"].append(new_tx)
        save_raw_data(data)
        self.reload_data()
        return True, "Peminjaman buku berhasil dicatat!"

    def return_book(self, book_id):
        data = load_raw_data()
        
        tx_target = next((t for t in data["transactions"] if t["book_id"] == book_id and t["return_date"] is None), None)
        if not tx_target:
            return False, "Tidak ada rekaman peminjaman aktif untuk buku ini."

        book_target = next((b for b in data["books"] if b["id"] == book_id), None)
        member_target = next((m for m in data["members"] if m["id"] == tx_target["member_id"]), None)

        tx_target["return_date"] = datetime.now().strftime("%Y-%m-%d %H:%M")
        if book_target:
            book_target["status"] = "Tersedia"
        if member_target:
            member_target["active_borrowings"] = max(0, member_target["active_borrowings"] - 1)

        self.undo_stack.push({
            "tx_id": tx_target["tx_id"],
            "book_id": book_id,
            "member_id": tx_target["member_id"]
        })

        save_raw_data(data)
        self.reload_data()
        if not self.reservation_queue.is_empty():
            next_reserve = self.reservation_queue.peek()
            if next_reserve["book_id"] == book_id:
                # Sampaikan informasi via GUI nanti bahwa antrean teratas siap mengambil buku
                next_user = self.reservation_queue.dequeue()
                return True, f"Buku dikembalikan! Antrean berikutnya (ID Member: {next_user['member_id']}) kini dapat memproses peminjaman."

        return True, "Buku berhasil dikembalikan!"

    def undo_last_return(self):
        if self.undo_stack.is_empty():
            return False, "Tidak ada transaksi pengembalian yang dapat dibatalkan!"

        last_action = self.undo_stack.pop()
        data = load_raw_data()

        tx_target = next((t for t in data["transactions"] if t["tx_id"] == last_action["tx_id"]), None)
        book_target = next((b for b in data["books"] if b["id"] == last_action["book_id"]), None)
        member_target = next((m for m in data["members"] if m["id"] == last_action["member_id"]), None)

        if tx_target and book_target and member_target:
            tx_target["return_date"] = None
            book_target["status"] = "Dipinjam"
            member_target["active_borrowings"] += 1
            
            save_raw_data(data)
            self.reload_data()
            return True, f"Undo Berhasil! Buku '{book_target['title']}' diset kembali ke status Dipinjam."
        
        return False, "Gagal memproses pembatalan aksi."

    def get_book_recommendations(self, book_id):
        """Mendapatkan rekomendasi ID buku lain berdasarkan Graph relasi"""
        return self.relation_graph.get_recommendations(book_id)