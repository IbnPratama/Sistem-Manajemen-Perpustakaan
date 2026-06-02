import tkinter as tk
from tkinter import messagebox, ttk

from library_management.modules import books as book_module
from library_management.modules import members as member_module
from library_management.modules import transactions as trx_module


class TransactionView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f5f5")
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        top = tk.Frame(self, bg="#f5f5f5")
        top.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top, text="Transaksi Peminjaman", font=("Helvetica", 14, "bold"), bg="#f5f5f5").pack(side="left")

        filter_frame = tk.Frame(top, bg="#f5f5f5")
        filter_frame.pack(side="right")
        tk.Label(filter_frame, text="Filter:", bg="#f5f5f5").pack(side="left")
        self._filter_var = tk.StringVar(value="semua")
        for val, lbl in [("semua", "Semua"), ("dipinjam", "Dipinjam"), ("dikembalikan", "Dikembalikan")]:
            tk.Radiobutton(
                filter_frame, text=lbl, variable=self._filter_var, value=val, bg="#f5f5f5", command=self._load_table
            ).pack(side="left", padx=3)

        search_frame = tk.Frame(self, bg="#f5f5f5")
        search_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(search_frame, text="Cari:", bg="#f5f5f5").pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
        tk.Entry(search_frame, textvariable=self._search_var, width=25).pack(side="left", padx=4)

        cols = ("ID", "Anggota", "Buku", "Tgl Pinjam", "Tgl Kembali", "Status")
        self._tree = ttk.Treeview(self, columns=cols, show="headings", height=12)
        widths = [70, 150, 200, 130, 130, 90]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center")
        self._tree.pack(fill="both", expand=True, padx=10, pady=4)
        self._tree.tag_configure("dipinjam", background="#fff9c4")
        self._tree.tag_configure("dikembalikan", background="#e8f5e9")

        borrow_frame = tk.LabelFrame(self, text="Form Peminjaman Baru", bg="#f5f5f5", padx=8, pady=6)
        borrow_frame.pack(fill="x", padx=10, pady=(0, 4))

        tk.Label(borrow_frame, text="ID Anggota:", bg="#f5f5f5").grid(row=0, column=0, sticky="e", padx=4)
        self._member_var = tk.StringVar()
        self._member_combo = ttk.Combobox(borrow_frame, textvariable=self._member_var, width=25, state="readonly")
        self._member_combo.grid(row=0, column=1, padx=4)

        tk.Label(borrow_frame, text="ID Buku:", bg="#f5f5f5").grid(row=0, column=2, sticky="e", padx=4)
        self._book_var = tk.StringVar()
        self._book_combo = ttk.Combobox(borrow_frame, textvariable=self._book_var, width=30, state="readonly")
        self._book_combo.grid(row=0, column=3, padx=4)

        tk.Button(borrow_frame, text="Refresh Pilihan", command=self._refresh_combos).grid(row=0, column=4, padx=6)
        self._refresh_combos()

        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=4)
        tk.Button(btn_frame, text="Pinjam Buku", width=14, command=self._borrow).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Kembalikan", width=14, command=self._return).pack(side="left", padx=4)
        tk.Button(btn_frame, text="Hapus Record", width=14, command=self._delete).pack(side="left", padx=4)

        info_frame = tk.Frame(self, bg="#f5f5f5")
        info_frame.pack(fill="x", padx=10, pady=(0, 6))
        tk.Button(info_frame, text="Lihat Antrian Pengembalian", command=self._show_queue).pack(side="left", padx=4)
        tk.Button(info_frame, text="Lihat Riwayat (Stack)", command=self._show_stack).pack(side="left", padx=4)

    def _refresh_combos(self):
        members = member_module.get_members_sorted()
        self._member_combo["values"] = [f"{m['id']} — {m['name']}" for m in members]
        books = book_module.get_books_sorted("title")
        self._book_combo["values"] = [f"{b['id']} — {b['title']} (stok: {b['stock']})" for b in books]

    def _load_table(self, transactions=None):
        self._tree.delete(*self._tree.get_children())
        if transactions is None:
            transactions = trx_module.get_transactions_sorted("borrow_date")
        filt = self._filter_var.get()
        if filt != "semua":
            transactions = [t for t in transactions if t["status"] == filt]
        for t in transactions:
            tag = t["status"]
            self._tree.insert(
                "",
                "end",
                iid=t["id"],
                values=(
                    t["id"],
                    t["member_name"],
                    t["book_title"],
                    t["borrow_date"],
                    t["return_date"] or "-",
                    t["status"],
                ),
                tags=(tag,),
            )

    def _on_search(self):
        q = self._search_var.get().strip()
        if q:
            results = trx_module.search_transactions(q)
            self._load_table(results)
        else:
            self._load_table()

    def _get_selected_id(self):
        sel = self._tree.selection()
        if not sel:
            return None
        return sel[0]

    def _borrow(self):
        member_val = self._member_var.get()
        book_val = self._book_var.get()
        if not member_val or not book_val:
            messagebox.showwarning("Peringatan", "Pilih anggota dan buku terlebih dahulu")
            return
        member_id = member_val.split(" — ")[0].strip()
        book_id = book_val.split(" — ")[0].strip()
        success, msg = trx_module.borrow_book(member_id, book_id)
        if success:
            messagebox.showinfo("Sukses", msg)
            self._refresh_combos()
            self._load_table()
        else:
            messagebox.showerror("Gagal", msg)

    def _return(self):
        trx_id = self._get_selected_id()
        if not trx_id:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang akan dikembalikan")
            return
        success, msg = trx_module.return_book(trx_id)
        if success:
            messagebox.showinfo("Sukses", msg)
            self._refresh_combos()
            self._load_table()
        else:
            messagebox.showerror("Gagal", msg)

    def _delete(self):
        trx_id = self._get_selected_id()
        if not trx_id:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang akan dihapus")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus record ini?"):
            trx_module.delete_transaction(trx_id)
            messagebox.showinfo("Sukses", "Record berhasil dihapus")
            self._load_table()

    def _show_queue(self):
        q = trx_module.get_return_queue()
        win = tk.Toplevel(self)
        win.title("Antrian Pengembalian (Queue)")
        win.geometry("500x300")
        tk.Label(win, text=f"Total antrian: {len(q)} buku", font=("Helvetica", 11, "bold")).pack(pady=6)
        txt = tk.Text(win, font=("Courier", 10))
        txt.pack(fill="both", expand=True, padx=8, pady=4)
        items = q.to_list()
        if not items:
            txt.insert("end", "Tidak ada pinjaman aktif.")
        for i, t in enumerate(items, 1):
            txt.insert("end", f"{i}. [{t['id']}] {t['member_name']} — {t['book_title']} (sejak {t['borrow_date']})\n")
        txt.config(state="disabled")

    def _show_stack(self):
        stack = trx_module.get_history_stack()
        win = tk.Toplevel(self)
        win.title("Riwayat Transaksi (Stack — terbaru di atas)")
        win.geometry("500x350")
        tk.Label(win, text="Riwayat (urut terbaru di atas)", font=("Helvetica", 11, "bold")).pack(pady=6)
        txt = tk.Text(win, font=("Courier", 10))
        txt.pack(fill="both", expand=True, padx=8, pady=4)
        items = stack.to_list()[::-1]
        if not items:
            txt.insert("end", "Belum ada transaksi.")
        for i, t in enumerate(items, 1):
            txt.insert(
                "end", f"{i}. [{t['id']}] {t['member_name']} — {t['book_title']} | {t['status']} | {t['borrow_date']}\n"
            )
        txt.config(state="disabled")
