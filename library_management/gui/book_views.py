import tkinter as tk
from tkinter import messagebox, ttk

from library_management.core.algorithms import binary_search, merge_sort
from library_management.modules.books import create_book, delete_book, read_books, update_book


class BookView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Book Input Operations (CRUD)")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(form_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_id = ttk.Entry(form_frame)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Title:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_title = ttk.Entry(form_frame)
        self.ent_title.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Author:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_author = ttk.Entry(form_frame)
        self.ent_author.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Category:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_category = ttk.Entry(form_frame)
        self.ent_category.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Year:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_year = ttk.Entry(form_frame)
        self.ent_year.grid(row=4, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Create", command=self.add_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update", command=self.update_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_entries).pack(side=tk.LEFT, padx=2)

        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        search_frame = ttk.LabelFrame(right_frame, text="Search & Sorting Metrics")
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search ID:").pack(side=tk.LEFT, padx=5)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Binary Search", command=self.search_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Merge Sort Title", command=lambda: self.refresh_table("title")).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(search_frame, text="Merge Sort Year", command=lambda: self.refresh_table("year")).pack(
            side=tk.LEFT, padx=5
        )

        table_frame = ttk.Frame(right_frame)
        table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Title", "Author", "Category", "Year"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Title", text="Title")
        self.tree.heading("Author", text="Author")
        self.tree.heading("Category", text="Category")
        self.tree.heading("Year", text="Year")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh_table(self, sort_key="id"):
        for item in self.tree.get_children():
            self.tree.delete(item)
        books = read_books()
        books = merge_sort(books, sort_key)
        for b in books:
            self.tree.insert("", tk.END, values=(b["id"], b["title"], b["author"], b["category"], b["year"]))

    def search_item(self):
        target = self.ent_search.get()
        if not target:
            self.refresh_table()
            return
        books = read_books()
        books = merge_sort(books, "id")
        idx = binary_search(books, "id", target)
        for item in self.tree.get_children():
            self.tree.delete(item)
        if idx != -1:
            b = books[idx]
            self.tree.insert("", tk.END, values=(b["id"], b["title"], b["author"], b["category"], b["year"]))
        else:
            messagebox.showinfo("Not Found", "Book identity data not matching inside records.")

    def add_item(self):
        if create_book(
            self.ent_id.get(), self.ent_title.get(), self.ent_author.get(), self.ent_category.get(), self.ent_year.get()
        ):
            messagebox.showinfo("Success", "New library asset recorded successfully.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Validation failure. Invalid parameters or duplicate ID detected.")

    def update_item(self):
        if update_book(
            self.ent_id.get(), self.ent_title.get(), self.ent_author.get(), self.ent_category.get(), self.ent_year.get()
        ):
            messagebox.showinfo("Success", "Target element rewritten successfully.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Failed to resolve identifier target reference.")

    def delete_item(self):
        if delete_book(self.ent_id.get()):
            messagebox.showinfo("Success", "Record structural deletion verified.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Failed to locate target record node structure.")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_entries()
            self.ent_id.insert(0, values[0])
            self.ent_title.insert(0, values[1])
            self.ent_author.insert(0, values[2])
            self.ent_category.insert(0, values[3])
            self.ent_year.insert(0, values[4])

    def clear_entries(self):
        self.ent_id.delete(0, tk.END)
        self.ent_title.delete(0, tk.END)
        self.ent_author.delete(0, tk.END)
        self.ent_category.delete(0, tk.END)
        self.ent_year.delete(0, tk.END)
