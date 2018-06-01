class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None # Left child node
        self.right = None # Right child node
        self.parent = None
        self.is_threaded = False # is_threaded. Tem "Costura"?
        self.thread = None # "Costura"
        self.id = None # Leaf unique id

class BinaryTree:
    def __init__(self, root=Node()):
        self.root = root
        self.leafs = {}
        self.sigma = set()
        self.composing_states = {}
