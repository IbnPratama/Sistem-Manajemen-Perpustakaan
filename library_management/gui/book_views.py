import tkinter as tk
from tkinter import messagebox, ttk

from library_management.modules import books as book_module


class BookView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f5f5")
        self._selected_id = None
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        top = tk.Frame(self, bg="#f5f5f5")
        top.pack(fill="x", padx=10, pady=(10, 0))

        tk.Label(top, text="Manajemen Buku", font=("Helvetica", 14, "bold"), bg="#f5f5f5").pack(side="left")

        search_frame = tk.Frame(top, bg="#f5f5f5")
        search_frame.pack(side="right")
        tk.Label(search_frame, text="Cari:", bg="#f5f5f5").pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
        tk.Entry(search_frame, textvariable=self._search_var, width=20).pack(side="left", padx=4)

        sort_frame = tk.Frame(self, bg="#f5f5f5")
        sort_frame.pack(fill="x", padx=10, pady=2)
        tk.Label(sort_frame, text="Urutkan:", bg="#f5f5f5").pack(side="left")
        self._sort_var = tk.StringVar(value="title")
        for val, label in [("title", "Judul"), ("author", "Penulis"), ("year", "Tahun")]:
            tk.Radiobutton(
                sort_frame, text=label, variable=self._sort_var, value=val, bg="#f5f5f5", command=self._load_table
            ).pack(side="left", padx=4)

        cols = ("ID", "Judul", "Penulis", "Tahun", "Genre", "Stok")
        self._tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        widths = [70, 220, 150, 60, 100, 50]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center")
        self._tree.pack(fill="both", expand=True, padx=10, pady=4)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        form_frame = tk.LabelFrame(self, text="Form Buku", bg="#f5f5f5", padx=8, pady=6)
        form_frame.pack(fill="x", padx=10, pady=(0, 4))

        labels = ["Judul", "Penulis", "Tahun", "Genre", "Stok"]
        self._entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(form_frame, text=lbl + ":", bg="#f5f5f5").grid(row=0, column=i * 2, sticky="e", padx=(4, 2))
            ent = tk.Entry(form_frame, width=14)
            ent.grid(row=0, column=i * 2 + 1, padx=(0, 6))
            self._entries[lbl.lower()] = ent

        btn_frame = tk.Frame(self, bg="#f5f5f5")
        btn_frame.pack(pady=4)
        for text, cmd in [
            ("Tambah", self._add),
            ("Update", self._update),
            ("Hapus", self._delete),
            ("Reset", self._reset),
        ]:
            tk.Button(btn_frame, text=text, width=10, command=cmd).pack(side="left", padx=4)

    def _load_table(self, books=None):
        self._tree.delete(*self._tree.get_children())
        if books is None:
            books = book_module.get_books_sorted(self._sort_var.get())
        for b in books:
            self._tree.insert(
                "", "end", iid=b["id"], values=(b["id"], b["title"], b["author"], b["year"], b["genre"], b["stock"])
            )

    def _on_search(self):
        q = self._search_var.get().strip()
        if q:
            results = book_module.search_books(q)
            self._load_table(results)
        else:
            self._load_table()

    def _on_select(self, _):
        sel = self._tree.selection()
        if not sel:
            return
        self._selected_id = sel[0]
        book = book_module.get_book_by_id(self._selected_id)
        if book:
            self._entries["judul"].delete(0, "end")
            self._entries["judul"].insert(0, book["title"])
            self._entries["penulis"].delete(0, "end")
            self._entries["penulis"].insert(0, book["author"])
            self._entries["tahun"].delete(0, "end")
            self._entries["tahun"].insert(0, str(book["year"]))
            self._entries["genre"].delete(0, "end")
            self._entries["genre"].insert(0, book["genre"])
            self._entries["stok"].delete(0, "end")
            self._entries["stok"].insert(0, str(book["stock"]))

    def _get_form(self):
        return (
            self._entries["judul"].get().strip(),
            self._entries["penulis"].get().strip(),
            self._entries["tahun"].get().strip(),
            self._entries["genre"].get().strip(),
            self._entries["stok"].get().strip(),
        )

    def _validate(self, title, author, year, genre, stock):
        if not all([title, author, year, genre, stock]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi")
            return False
        try:
            int(year)
            int(stock)
        except ValueError:
            messagebox.showwarning("Peringatan", "Tahun dan stok harus angka")
            return False
        return True

    def _add(self):
        title, author, year, genre, stock = self._get_form()
        if not self._validate(title, author, year, genre, stock):
            return
        book_module.add_book(title, author, year, genre, stock)
        messagebox.showinfo("Sukses", "Buku berhasil ditambahkan")
        self._reset()
        self._load_table()

    def _update(self):
        if not self._selected_id:
            messagebox.showwarning("Peringatan", "Pilih buku yang akan diupdate")
            return
        title, author, year, genre, stock = self._get_form()
        if not self._validate(title, author, year, genre, stock):
            return
        book_module.update_book(self._selected_id, title, author, year, genre, stock)
        messagebox.showinfo("Sukses", "Buku berhasil diupdate")
        self._reset()
        self._load_table()

    def _delete(self):
        if not self._selected_id:
            messagebox.showwarning("Peringatan", "Pilih buku yang akan dihapus")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?"):
            book_module.delete_book(self._selected_id)
            messagebox.showinfo("Sukses", "Buku berhasil dihapus")
            self._reset()
            self._load_table()

    def _reset(self):
        self._selected_id = None
        for ent in self._entries.values():
            ent.delete(0, "end")
        self._tree.selection_remove(self._tree.selection())
