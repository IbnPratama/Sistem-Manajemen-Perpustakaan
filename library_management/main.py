import tkinter as tk
from tkinter import ttk
from library_management.gui.book_views import BookView
from library_management.gui.member_view import MemberView
from library_management.gui.transaction_view import TransactionView

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Library Management Workspace")
        self.geometry("950x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        book_frame = BookView(notebook)
        member_frame = MemberView(notebook)
        tx_frame = TransactionView(notebook)

        notebook.add(book_frame, text="Books Catalog View")
        notebook.add(member_frame, text="Membership Subsystem")
        notebook.add(tx_frame, text="Circulation Matrix Dashboard")

        notebook.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_change(book_frame, member_frame, tx_frame))

    def on_tab_change(self, b_f, m_f, t_f):
        b_f.refresh_table()
        m_f.refresh_table()
        t_f.refresh_all()

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()