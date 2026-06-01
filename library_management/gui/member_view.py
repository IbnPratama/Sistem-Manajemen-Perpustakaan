import tkinter as tk
from tkinter import messagebox, ttk


class MemberView:
    def __init__(self, parent, member_module):
        self.parent = parent
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
        title_label = ttk.Label(self.frame, text="Manajemen Anggota", style="Title.TLabel")
        title_label.pack(pady=(0, 20))

        form_frame = ttk.LabelFrame(self.frame, text="Form Anggota", padding="20")
        form_frame.pack(fill=tk.X, pady=10)

        ttk.Label(form_frame, text="ID Anggota:").grid(row=0, column=0, sticky=tk.W, pady=8)
        self.id_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.id_entry.grid(row=0, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Nama:").grid(row=1, column=0, sticky=tk.W, pady=8)
        self.name_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.name_entry.grid(row=1, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=8)
        self.email_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.email_entry.grid(row=2, column=1, pady=8, padx=10)

        ttk.Label(form_frame, text="Telepon:").grid(row=3, column=0, sticky=tk.W, pady=8)
        self.phone_entry = ttk.Entry(form_frame, width=35, font=("Segoe UI", 10))
        self.phone_entry.grid(row=3, column=1, pady=8, padx=10)

        btn_frame = ttk.Frame(self.frame)
        btn_frame.pack(fill=tk.X, pady=15)

        ttk.Button(btn_frame, text="Tambah", command=self.add_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Update", command=self.update_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Hapus", command=self.delete_member).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_list).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Form", command=self.clear_entries).pack(side=tk.LEFT, padx=5)

        columns = ("id", "nama", "email", "telepon")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID Anggota")
        self.tree.heading("nama", text="Nama")
        self.tree.heading("email", text="Email")
        self.tree.heading("telepon", text="Telepon")

        self.tree.column("id", width=100, anchor=tk.CENTER)
        self.tree.column("nama", width=250, anchor=tk.W)
        self.tree.column("email", width=200, anchor=tk.W)
        self.tree.column("telepon", width=150, anchor=tk.CENTER)

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
            self.name_entry.delete(0, tk.END)
            self.name_entry.insert(0, item["values"][1])
            self.email_entry.delete(0, tk.END)
            self.email_entry.insert(0, item["values"][2])
            self.phone_entry.delete(0, tk.END)
            self.phone_entry.insert(0, item["values"][3])

    def clear_entries(self):
        self.id_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)

    def add_member(self):
        member_id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if not member_id or not name or not email or not phone:
            messagebox.showwarning("Peringatan", "Semua field harus diisi!")
            return
        self.member_module.create(member_id, name, email, phone)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan!")

    def update_member(self):
        member_id = self.id_entry.get()
        name = self.name_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        if not member_id:
            messagebox.showwarning("Peringatan", "Pilih anggota yang ingin diupdate!")
            return
        self.member_module.update(member_id, name, email, phone)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Anggota berhasil diupdate!")

    def delete_member(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih anggota yang ingin dihapus!")
            return
        member_id = self.tree.item(selected[0])["values"][0]
        self.member_module.delete(member_id)
        self.clear_entries()
        self.refresh_list()
        messagebox.showinfo("Sukses", "Anggota berhasil dihapus!")

    def refresh_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        members = self.member_module.read_all()
        for member in members:
            self.tree.insert(
                "", tk.END, values=(member.get("id"), member.get("name"), member.get("email"), member.get("phone"))
            )
