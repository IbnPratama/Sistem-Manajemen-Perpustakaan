import tkinter as tk
from tkinter import messagebox, ttk

from library_management.modules import members as member_module


class MemberView(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#f5f5f5")
        self._selected_id = None
        self._build_ui()
        self._load_table()

    def _build_ui(self):
        top = tk.Frame(self, bg="#f5f5f5")
        top.pack(fill="x", padx=10, pady=(10, 0))
        tk.Label(top, text="Manajemen Anggota", font=("Helvetica", 14, "bold"), bg="#f5f5f5").pack(side="left")

        search_frame = tk.Frame(top, bg="#f5f5f5")
        search_frame.pack(side="right")
        tk.Label(search_frame, text="Cari:", bg="#f5f5f5").pack(side="left")
        self._search_var = tk.StringVar()
        self._search_var.trace_add("write", lambda *_: self._on_search())
        tk.Entry(search_frame, textvariable=self._search_var, width=20).pack(side="left", padx=4)

        cols = ("ID", "Nama", "Email", "Telepon", "Pinjaman Aktif")
        self._tree = ttk.Treeview(self, columns=cols, show="headings", height=14)
        widths = [70, 180, 200, 120, 100]
        for col, w in zip(cols, widths):
            self._tree.heading(col, text=col)
            self._tree.column(col, width=w, anchor="center")
        self._tree.pack(fill="both", expand=True, padx=10, pady=4)
        self._tree.bind("<<TreeviewSelect>>", self._on_select)

        form_frame = tk.LabelFrame(self, text="Form Anggota", bg="#f5f5f5", padx=8, pady=6)
        form_frame.pack(fill="x", padx=10, pady=(0, 4))

        labels = ["Nama", "Email", "Telepon"]
        self._entries = {}
        for i, lbl in enumerate(labels):
            tk.Label(form_frame, text=lbl + ":", bg="#f5f5f5").grid(row=0, column=i * 2, sticky="e", padx=(4, 2))
            ent = tk.Entry(form_frame, width=20)
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

    def _load_table(self, members=None):
        self._tree.delete(*self._tree.get_children())
        if members is None:
            members = member_module.get_members_sorted()
        for m in members:
            self._tree.insert(
                "", "end", iid=m["id"], values=(m["id"], m["name"], m["email"], m["phone"], m.get("active_loans", 0))
            )

    def _on_search(self):
        q = self._search_var.get().strip()
        if q:
            results = member_module.search_members(q)
            self._load_table(results)
        else:
            self._load_table()

    def _on_select(self, _):
        sel = self._tree.selection()
        if not sel:
            return
        self._selected_id = sel[0]
        member = member_module.get_member_by_id(self._selected_id)
        if member:
            self._entries["nama"].delete(0, "end")
            self._entries["nama"].insert(0, member["name"])
            self._entries["email"].delete(0, "end")
            self._entries["email"].insert(0, member["email"])
            self._entries["telepon"].delete(0, "end")
            self._entries["telepon"].insert(0, member["phone"])

    def _get_form(self):
        return (
            self._entries["nama"].get().strip(),
            self._entries["email"].get().strip(),
            self._entries["telepon"].get().strip(),
        )

    def _validate(self, name, email, phone):
        if not all([name, email, phone]):
            messagebox.showwarning("Peringatan", "Semua field harus diisi")
            return False
        return True

    def _add(self):
        name, email, phone = self._get_form()
        if not self._validate(name, email, phone):
            return
        member_module.add_member(name, email, phone)
        messagebox.showinfo("Sukses", "Anggota berhasil ditambahkan")
        self._reset()
        self._load_table()

    def _update(self):
        if not self._selected_id:
            messagebox.showwarning("Peringatan", "Pilih anggota yang akan diupdate")
            return
        name, email, phone = self._get_form()
        if not self._validate(name, email, phone):
            return
        member_module.update_member(self._selected_id, name, email, phone)
        messagebox.showinfo("Sukses", "Anggota berhasil diupdate")
        self._reset()
        self._load_table()

    def _delete(self):
        if not self._selected_id:
            messagebox.showwarning("Peringatan", "Pilih anggota yang akan dihapus")
            return
        if messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus anggota ini?"):
            success, msg = member_module.delete_member(self._selected_id)
            if success:
                messagebox.showinfo("Sukses", msg)
                self._reset()
                self._load_table()
            else:
                messagebox.showerror("Gagal", msg)

    def _reset(self):
        self._selected_id = None
        for ent in self._entries.values():
            ent.delete(0, "end")
        self._tree.selection_remove(self._tree.selection())
