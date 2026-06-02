import tkinter as tk
from tkinter import messagebox, ttk

from library_management.core.algorithms import binary_search, merge_sort
from library_management.modules.members import create_member, delete_member, read_members, update_member


class MemberView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.refresh_table()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Member Registry Portal")
        form_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(form_frame, text="Member ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_id = ttk.Entry(form_frame)
        self.ent_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Name:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_name = ttk.Entry(form_frame)
        self.ent_name.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_email = ttk.Entry(form_frame)
        self.ent_email.grid(row=2, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)

        ttk.Button(btn_frame, text="Create", command=self.add_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Update", command=self.update_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="Clear", command=self.clear_entries).pack(side=tk.LEFT, padx=2)

        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        search_frame = ttk.LabelFrame(right_frame, text="Query Mechanics")
        search_frame.pack(side=tk.TOP, fill=tk.X, pady=5)

        ttk.Label(search_frame, text="Search ID:").pack(side=tk.LEFT, padx=5)
        self.ent_search = ttk.Entry(search_frame)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Binary Search", command=self.search_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(search_frame, text="Merge Sort Name", command=lambda: self.refresh_table("name")).pack(
            side=tk.LEFT, padx=5
        )

        table_frame = ttk.Frame(right_frame)
        table_frame.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Email"), show="headings")
        self.tree.heading("ID", text="Member ID")
        self.tree.heading("Name", text="Full Name")
        self.tree.heading("Email", text="Email Address")
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

    def refresh_table(self, sort_key="id"):
        for item in self.tree.get_children():
            self.tree.delete(item)
        members = read_members()
        members = merge_sort(members, sort_key)
        for m in members:
            self.tree.insert("", tk.END, values=(m["id"], m["name"], m["email"]))

    def search_item(self):
        target = self.ent_search.get()
        if not target:
            self.refresh_table()
            return
        members = read_members()
        members = merge_sort(members, "id")
        idx = binary_search(members, "id", target)
        for item in self.tree.get_children():
            self.tree.delete(item)
        if idx != -1:
            m = members[idx]
            self.tree.insert("", tk.END, values=(m["id"], m["name"], m["email"]))
        else:
            messagebox.showinfo("Not Found", "Member identity records yielded empty response.")

    def add_item(self):
        if create_member(self.ent_id.get(), self.ent_name.get(), self.ent_email.get()):
            messagebox.showinfo("Success", "User structure instantiated.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Validation failure parameters.")

    def update_item(self):
        if update_member(self.ent_id.get(), self.ent_name.get(), self.ent_email.get()):
            messagebox.showinfo("Success", "Structural memory field updated.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Identifier target mismatch.")

    def delete_item(self):
        if delete_member(self.ent_id.get()):
            messagebox.showinfo("Success", "Target element discarded from storage node.")
            self.refresh_table()
            self.clear_entries()
        else:
            messagebox.showerror("Error", "Failed deletion execution sequence.")

    def on_select(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0], "values")
            self.clear_entries()
            self.ent_id.insert(0, values[0])
            self.ent_name.insert(0, values[1])
            self.ent_email.insert(0, values[2])

    def clear_entries(self):
        self.ent_id.delete(0, tk.END)
        self.ent_name.delete(0, tk.END)
        self.ent_email.delete(0, tk.END)
