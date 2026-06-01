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

    def from_list(self, py_list):
        self.head = None
        for item in py_list:
            self.append(item)


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


class BSTNode:
    def __init__(self, key, value):
        self.key = key        
        self.value = value    
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, key, value):
        new_node = BSTNode(key, value)
        if self.root is None:
            self.root = new_node
        else:
            self._insert_recursive(self.root, new_node)

    def _insert_recursive(self, current, new_node):
        if new_node.key < current.key:
            if current.left is None:
                current.left = new_node
            else:
                self._insert_recursive(current.left, new_node)
        else:
            if current.right is None:
                current.right = new_node
            else:
                self._insert_recursive(current.right, new_node)

    def search(self, key):
        return self._search_recursive(self.root, key)

    def _search_recursive(self, current, key):
        if current is None or current.key == key:
            return current.value if current else None
        if key < current.key:
            return self._search_recursive(current.left, key)
        return self._search_recursive(current.right, key)


class HashMap:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(self.size)]  

    def _hash(self, key):
        return sum(ord(char) for char in str(key)) % self.size

    def put(self, key, value):
        hash_index = self._hash(key)
        for pair in self.table[hash_index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[hash_index].append([key, value])

    def get(self, key):
        hash_index = self._hash(key)
        for pair in self.table[hash_index]:
            if pair[0] == key:
                return pair[1]
        return None


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
            self.adjacency_list[book_id2].append(book_id1)

    def get_recommendations(self, book_id):
        return self.adjacency_list.get(book_id, [])