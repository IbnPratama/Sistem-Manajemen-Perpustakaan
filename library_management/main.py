import json
import os
import tkinter as tk
from tkinter import ttk

from library_management.gui.book_views import BookView
from library_management.gui.member_view import MemberView
from library_management.gui.transaction_view import TransactionView

DATA_PATH = os.path.join(os.path.dirname(__file__), "data.json")


def _init_data():
    if not os.path.exists(DATA_PATH):
        with open(DATA_PATH, "w") as f:
            json.dump({"books": [], "members": [], "transactions": []}, f, indent=2)
    else:
        with open(DATA_PATH, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
        changed = False
        for key in ("books", "members", "transactions"):
            if key not in data:
                data[key] = []
                changed = True
        if changed:
            with open(DATA_PATH, "w") as f:
                json.dump(data, f, indent=2)


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sistem Manajemen Perpustakaan")
        self.geometry("900x680")
        self.resizable(True, True)
        self.configure(bg="#f5f5f5")
        self._build_ui()

    def _build_ui(self):
        header = tk.Frame(self, bg="#1a237e", height=50)
        header.pack(fill="x")
        tk.Label(
            header, text="📚 Sistem Manajemen Perpustakaan", font=("Helvetica", 15, "bold"), fg="white", bg="#1a237e"
        ).pack(side="left", padx=16, pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=6, pady=6)

        book_tab = BookView(notebook)
        member_tab = MemberView(notebook)
        trx_tab = TransactionView(notebook)

        notebook.add(book_tab, text="  📖 Buku  ")
        notebook.add(member_tab, text="  👤 Anggota  ")
        notebook.add(trx_tab, text="  🔄 Transaksi  ")

        status = tk.Frame(self, bg="#e0e0e0", height=24)
        status.pack(fill="x", side="bottom")
        tk.Label(status, text="Library Management System — UAP Praktikum", bg="#e0e0e0", font=("Helvetica", 9)).pack(
            side="left", padx=8
        )


def main():
    _init_data()
    app = MainApp()
    app.mainloop()


if __name__ == "__main__":
    main()
