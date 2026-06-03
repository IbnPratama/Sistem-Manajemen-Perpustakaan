class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = node
            node.prev = current
        self._size += 1

    def remove(self, key_func):
        current = self.head
        while current:
            if key_func(current.data):
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                if current.next:
                    current.next.prev = current.prev
                self._size -= 1
                return True
            current = current.next
        return False

    def find(self, key_func):
        current = self.head
        while current:
            if key_func(current.data):
                return current.data
            current = current.next
        return None

    def to_list(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self._size


class Stack:
    def __init__(self):
        self._data = []

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            return None
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            return None
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


class Queue:
    def __init__(self):
        self._data = []

    def enqueue(self, item):
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            return None
        return self._data.pop(0)

    def peek(self):
        if self.is_empty():
            return None
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def __len__(self):
        return len(self._data)

    def to_list(self):
        return list(self._data)


class HashTable:
    def __init__(self, size=64):
        self._size = size
        self._buckets = [[] for _ in range(self._size)]

    def _hash(self, key):
        return hash(str(key)) % self._size

    def insert(self, key, value):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        bucket.append((key, value))

    def get(self, key):
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return None

    def delete(self, key):
        idx = self._hash(key)
        bucket = self._buckets[idx]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                return True
        return False

    def keys(self):
        result = []
        for bucket in self._buckets:
            for k, _ in bucket:
                result.append(k)
        return result

    def values(self):
        result = []
        for bucket in self._buckets:
            for _, v in bucket:
                result.append(v)
        return result

    def items(self):
        result = []
        for bucket in self._buckets:
            for pair in bucket:
                result.append(pair)
        return result


class BSTNode:
    def __init__(self, key, data):
        self.key = key
        self.data = data
        self.left = None
        self.right = None


class BST:
    def __init__(self):
        self.root = None

    def insert(self, key, data):
        self.root = self._insert(self.root, key, data)

    def _insert(self, node, key, data):
        if node is None:
            return BSTNode(key, data)
        if key < node.key:
            node.left = self._insert(node.left, key, data)
        elif key > node.key:
            node.right = self._insert(node.right, key, data)
        else:
            node.data = data
        return node

    def search(self, key):
        return self._search(self.root, key)

    def _search(self, node, key):
        if node is None:
            return None
        if key == node.key:
            return node.data
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)

    def delete(self, key):
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        if node is None:
            return None
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            min_node = self._find_min(node.right)
            node.key = min_node.key
            node.data = min_node.data
            node.right = self._delete(node.right, min_node.key)
        return node

    def _find_min(self, node):
        while node.left:
            node = node.left
        return node

    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result

    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append(node.data)
            self._inorder(node.right, result)
        

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
