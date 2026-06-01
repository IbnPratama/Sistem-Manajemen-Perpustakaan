import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class TransactionView:
    def __init__(self, parent, transaction_module, book_module, member_module):
        self.parent = parent
        self.transaction_module = transaction_module
        self.book_module = book_module
        self.member_module = member_module
        self.frame = ttk.Frame(parent, padding="30")
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10, "bold"), padding=5)
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))
        style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)
        style.configure("Title.TLabel", font=("Segoe UI", 18, "bold"), foreground="#2c3e50")

    def setup_ui(self):
        title_label = ttk.Label(self.frame, text="Transaksi Peminjaman", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        form_frame = ttk.LabelFrame(self.frame, text="Form Transaksi", padding="20")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="ID Transaksi:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.trans_id_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.trans_id_entry.grid(row=0, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="ID Anggota:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.member_id_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.member_id_entry.grid(row=1, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="ID Buku:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.book_id_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.book_id_entry.grid(row=2, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Tanggal Pinjam:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.borrow_date_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.borrow_date_entry.grid(row=3, column=1, pady=8, padx=10)
        self.borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=15)

        ttk.Button(btn_frame, text="Pinjam Buku", command=self.borrow_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Kembalikan Buku", command=self.return_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_entries).pack(side=tk.LEFT, padx=5)

        columns = ("id", "id_anggota", "id_buku", "tgl_pinjam", "tgl_kembali", "status")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID Transaksi")
        self.tree.heading("id_anggota", text="ID Anggota")
        self.tree.heading("id_buku", text="ID Buku")
        self.tree.heading("tgl_pinjam", text="Tgl Pinjam")
        self.tree.heading("tgl_kembali", text="Tgl Kembali")
        self.tree.heading("status", text="Status")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("id_anggota", width=100, anchor=tk.CENTER)
        self.tree.column("id_buku", width=100, anchor=tk.CENTER)
        self.tree.column("tgl_pinjam", width=120, anchor=tk.CENTER)
        self.tree.column("tgl_kembali", width=120, anchor=tk.CENTER)
        self.tree.column("status", width=100, anchor=tk.CENTER)

        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.refresh_list()

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.trans_id_entry.delete(0, tk.END)
            self.trans_id_entry.insert(0, item["values"][0])
            self.member_id_entry.delete(0, tk.END)
            self.member_id_entry.insert(0, item["values"][1])
            self.book_id_entry.delete(0, tk.END)
            self.book_id_entry.insert(0, item["values"][2])
            self.borrow_date_entry.delete(0, tk.END)
            self.borrow_date_entry.insert(0, item["values"][3])

    def clear_entries(self):
        self.trans_id_entry.delete(0, tk.END)
        self.member_id_entry.delete(0, tk.END)
        self.book_id_entry.delete(0, tk.END)
        self.borrow_date_entry.delete(0, tk.END)
        self.borrow_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

    def borrow_book(self):
        trans_id = self.trans_id_entry.get()
        member_id = self.member_id_entry.get()
        book_id = self.book_id_entry.get()
        borrow_date = self.borrow_date_entry.get()
        if not trans_id or not member_id or not book_id or not borrow_date:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        self.transaction_module.borrow(trans_id, member_id, book_id, borrow_date)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Buku berhasil dipinjam!")

    def return_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih transaksi yang ingin dikembalikan!")
            return
        trans_id = self.tree.item(selected[0])["values"][0]
        self.transaction_module.return_book(trans_id, datetime.now().strftime("%Y-%m-%d"))
        self.refresh_list()
        messagebox.showinfo("Sukses", "Buku berhasil dikembalikan!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        transactions = self.transaction_module.read_all()
        for trans in transactions:
            self.tree.insert(
                "",
                tk.END,
                values=(
                    trans.get("id"),
                    trans.get("member_id"),
                    trans.get("book_id"),
                    trans.get("borrow_date"),
                    trans.get("return_date", "-"),
                    trans.get("status"),
                ),
            )
