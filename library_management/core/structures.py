class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

class Queue:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return len(self.items) == 0

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
class HashTable:
    def __init__(self, size=50):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def insert(self, key, value):
        hash_index = self._hash(key)
        for kv in self.table[hash_index]:
            if kv[0] == key:
                kv[1] = value
                return
        self.table[hash_index].append([key, value])

    def get(self, key):
        hash_index = self._hash(key)
        for kv in self.table[hash_index]:
            if kv[0] == key:
                return kv[1]
        return None

    def delete(self, key):
        hash_index = self._hash(key)
        for i, kv in enumerate(self.table[hash_index]):
            if kv[0] == key:
                del self.table[hash_index][i]
                return True
        return False

class BSTNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        if not self.root:
            self.root = BSTNode(key, data)
        else:
            self._insert_recursive(self.root, key, data)

    def _insert_recursive(self, current, key, data):
        if key < current.key:
            if current.left is None:
                current.left = BSTNode(key, data)
            else:
                self._insert_recursive(current.left, key, data)
        else:
            if current.right is None:
                current.right = BSTNode(key, data)
            else:
                self._insert_recursive(current.right, key, data)

    def inorder_traversal(self):
        result = []
        self._inorder_recursive(self.root, result)
        return result

    def _inorder_recursive(self, current, result):
        if current:
            self._inorder_recursive(current.left, result)
            result.append(current.data)
            self._inorder_recursive(current.right, result)

class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, book_id):
        if book_id not in self.adjacency_list:
            self.adjacency_list[book_id] = []

    def add_edge(self, book_id1, book_id2):
        self.add_vertex(book_id1)
        self.add_vertex(book_id2)
        if book_id2 not in self.adjacency_list[book_id1]:
            self.adjacency_list[book_id1].append(book_id2)
        if book_id1 not in self.adjacency_list[book_id2]:
            self.adjacency_list[book_id2].append(book_id2) 

    def get_recommendations(self, book_id):
        return self.adjacency_list.get(book_id, [])