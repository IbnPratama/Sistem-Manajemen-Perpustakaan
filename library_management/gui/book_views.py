import tkinter as tk
from tkinter import messagebox, ttk


class BookView:
    def __init__(self, parent, book_module):
        self.parent = parent
        self.book_module = book_module
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
        title_label = ttk.Label(self.frame, text="Manajemen Buku", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        form_frame = ttk.LabelFrame(self.frame, text="Form Buku", padding="20")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="ID Buku:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.id_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.id_entry.grid(row=0, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Judul:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.title_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.title_entry.grid(row=1, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Penulis:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.author_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.author_entry.grid(row=2, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Tahun:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.year_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.year_entry.grid(row=3, column=1, pady=8, padx=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=15)

        ttk.Button(btn_frame, text="Tambah", command=self.add_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.delete_book).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_entries).pack(side=tk.LEFT, padx=5)

        columns = ("id", "judul", "penulis", "tahun")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID Buku")
        self.tree.heading("judul", text="Judul")
        self.tree.heading("penulis", text="Penulis")
        self.tree.heading("tahun", text="Tahun")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("judul", width=300, anchor=tk.W)
        self.tree.column("penulis", width=200, anchor=tk.W)
        self.tree.column("tahun", width=100, anchor=tk.CENTER)

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
            self.id_entry.delete(0, tk.END)
            self.id_entry.insert(0, item["values"][0])
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, item["values"][1])
            self.author_entry.delete(0, tk.END)
            self.author_entry.insert(0, item["values"][2])
            self.year_entry.delete(0, tk.END)
            self.year_entry.insert(0, item["values"][3])

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)

    def add_book(self):
        book_id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        if not book_id or not title or not author or not year:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        self.book_module.create(book_id, title, author, year)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Buku berhasil ditambahkan!")

    def update_book(self):
        book_id = self.id_entry.get()
        title = self.title_entry.get()
        author = self.author_entry.get()
        year = self.year_entry.get()
        if not book_id:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin diupdate!")
            return
        self.book_module.update(book_id, title, author, year)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Buku berhasil diupdate!")

    def delete_book(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih buku yang ingin dihapus!")
            return
        book_id = self.tree.item(selected[0])["values"][0]
        self.book_module.delete(book_id)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Buku berhasil dihapus!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        books = self.book_module.read_all()
        for book in books:
            self.tree.insert(
                "", tk.END, values=(book.get("id"), book.get("title"), book.get("author"), book.get("year"))
            )
