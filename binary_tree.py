class Node:
    def __init__(self, value=None):
        self.value = value
        self.l = None # Left child node
        self.r = None # Right child node
        self.n = None # Next is about threaded binary trees -> "Costura"

class BinaryTree:
    def __init__(self, root=Node()):
        self.root = root
