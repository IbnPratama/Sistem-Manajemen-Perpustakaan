import tkinter as tk
from tkinter import messagebox, ttk

from library_management.core.structures import LinkedList, Queue, Stack, TreeNode
from library_management.modules.transactions import add_reservation, borrow_book, load_data, return_book


class TransactionView(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill=tk.BOTH, expand=True)
        self.create_widgets()
        self.refresh_all()

    def create_widgets(self):
        ops_frame = ttk.LabelFrame(self, text="Circulation Commands")
        ops_frame.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)

        ttk.Label(ops_frame, text="Book ID:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_book_id = ttk.Entry(ops_frame)
        self.ent_book_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(ops_frame, text="Member ID:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.ent_member_id = ttk.Entry(ops_frame)
        self.ent_member_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(ops_frame, text="Issue Loan", command=self.do_borrow).grid(
            row=2, column=0, columnspan=2, pady=5, sticky=tk.EW
        )
        ttk.Button(ops_frame, text="Process Return", command=self.do_return).grid(
            row=3, column=0, columnspan=2, pady=5, sticky=tk.EW
        )
        ttk.Button(ops_frame, text="Queue Reservation", command=self.do_reserve).grid(
            row=4, column=0, columnspan=2, pady=5, sticky=tk.EW
        )

        right_frame = ttk.Frame(self)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        notebook = ttk.Notebook(right_frame)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.tx_tree = ttk.Treeview(notebook, columns=("TxID", "BookID", "MemberID", "Date", "Status"), show="headings")
        self.tx_tree.heading("TxID", text="Tx ID")
        self.tx_tree.heading("BookID", text="Book ID")
        self.tx_tree.heading("MemberID", text="Member ID")
        self.tx_tree.heading("Date", text="Borrow Date")
        self.tx_tree.heading("Status", text="Status")
        notebook.add(self.tx_tree, text="Active Loans (Linked List)")

        self.res_tree = ttk.Treeview(notebook, columns=("BookID", "MemberID"), show="headings")
        self.res_tree.heading("BookID", text="Book ID")
        self.res_tree.heading("MemberID", text="Member ID")
        notebook.add(self.res_tree, text="Reservations (Queue)")

        self.log_list = tk.Listbox(notebook)
        notebook.add(self.log_list, text="System Log Trace (Stack)")

        self.cat_tree_view = ttk.Treeview(notebook, columns=("Name"), show="tree")
        notebook.add(self.cat_tree_view, text="Classification (Tree)")

    def refresh_all(self):
        data = load_data()

        for item in self.tx_tree.get_children():
            self.tx_tree.delete(item)
        tx_ll = LinkedList()
        for t in data["transactions"]:
            tx_ll.append(t)
        for t in tx_ll.to_list():
            self.tx_tree.insert(
                "", tk.END, values=(t["tx_id"], t["book_id"], t["member_id"], t["borrow_date"], t["status"])
            )

        for item in self.res_tree.get_children():
            self.res_tree.delete(item)
        res_q = Queue()
        for r in data["reservations"]:
            res_q.enqueue(r)
        for r in res_q.to_list():
            self.res_tree.insert("", tk.END, values=(r["book_id"], r["member_id"]))

        self.log_list.delete(0, tk.END)
        log_stack = Stack()
        for log in data["logs"]:
            log_stack.push(log)
        for log in log_stack.to_list():
            self.log_list.insert(tk.END, log)

        for item in self.cat_tree_view.get_children():
            self.cat_tree_view.delete(item)
        root_node = TreeNode("Library Catalog Architecture")
        fiction = TreeNode("Fiction")
        fiction.add_child(TreeNode("Sci-Fi"))
        fiction.add_child(TreeNode("Fantasy"))
        non_fiction = TreeNode("Non-Fiction")
        non_fiction.add_child(TreeNode("History"))
        non_fiction.add_child(TreeNode("Biography"))
        root_node.add_child(fiction)
        root_node.add_child(non_fiction)

        def render_tree_nodes(parent_ui_id, structural_node):
            node_ui_id = self.cat_tree_view.insert(parent_ui_id, tk.END, text=structural_node.name, open=True)
            for child in structural_node.children:
                render_tree_nodes(node_ui_id, child)

        render_tree_nodes("", root_node)

    def do_borrow(self):
        success, msg = borrow_book(self.ent_book_id.get(), self.ent_member_id.get())
        if success:
            messagebox.showinfo("Success", "Transaction instance committed.")
            self.refresh_all()
        else:
            messagebox.showerror("Error", msg)

    def do_return(self):
        success, msg = return_book(self.ent_book_id.get())
        if success:
            messagebox.showinfo("Success", "State modification update completed.")
            self.refresh_all()
        else:
            messagebox.showerror("Error", msg)

    def do_reserve(self):
        if add_reservation(self.ent_book_id.get(), self.ent_member_id.get()):
            messagebox.showinfo("Success", "Element scheduled into internal Queue structure.")
            self.refresh_all()
        else:
            messagebox.showerror("Error", "Reference verification error during execution.")
