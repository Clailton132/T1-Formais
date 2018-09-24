#!/usr/bin/env python

"""
    Classe Node
    Usada na árvore binária costurada
"""
class Node:
    def __init__(self, value=None):
        self.value = value
        self.left = None # Left child node
        self.right = None # Right child node
        self.parent = None
        self.is_threaded = False # is_threaded. Tem "Costura"?
        self.thread = None # "Costura"
        self.id = None # Leaf unique id


"""
    Class BinaryTree
    Árvore binária costurada utilizada no algoritmo De Simone para realizar
    a transformação de expressões regulares em autômatos finitos
"""
class BinaryTree:
    def __init__(self, root=Node()):
        self.root = root
        self.leafs = {}
        self.sigma = set()
        self.composing_states = {}
