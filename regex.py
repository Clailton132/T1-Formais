#!/usr/bin/env python
# -*- coding: utf-8 -*-

from binary_tree import *

"""
    Class Regex: Expressões Regulares
"""
class Regex:
    def  __init__(self):
        self.literal = ""
        self.E = []

    """
        Transforma uma entrada da forma String em uma lista de símbolos levando
        em consideração a ordem de precedência: 1)* 2). 3)|

        - Operadores '|', '?', '*' são representados como dicionários
        - Concatenações são representadas pela posição dos símbolos na lista

        Exemplo: (a|bc*) é representado por [{'|': [['a'], ['b'],{'*': 'c'}]}]
    """
    def set_regex(self, input):
        self.literal = input
        input = "("+input+")"
        self.E = []
        k = 0
        context = [[]]
        c = context[0]
        for i, char in enumerate(input):
            if char == '(':
                context.append([])
                k += 1
                c = context[k]
            elif char == ')':
                tmp = context[k]
                if "|" in tmp:
                    alternation = {"|": []}
                    aux = 0
                    size = len(tmp)
                    for j, item in enumerate(tmp):
                        if item == "|":
                            alternation["|"].append(tmp[aux: j])
                            aux = j + 1
                        if (j == size-1):
                            alternation["|"].append(tmp[aux:])
                    tmp = alternation
                context[k-1].append(tmp)
                del context[k]
                k -= 1
                c = context[k]
            elif char in ("*", "?"):
                if i > 0:
                    tmp = c[-1]
                    del c[-1]
                    c.append({char: tmp})
            elif char == "|":
                c.append("|")
            elif char == " ":
                pass
            else:
                c.append(char)
        self.E = context[0][0] # Validates context and normalize expression


    """
        Converte uma expressão regular em um autômato finito
        Utilizando o método De Simone
    """
    def get_equivalent_automata(self):
        tree = self.get_tree()
        self.fill_threaded_tree(tree)
        # self.print_threaded_tree(tree)
        fa = self.fill_composing_and_get_automata(tree)
        # self.print_composing(tree)
        return fa

    """
        Obtém a árvore binária costurada para conversão ER -> AF
    """
    def get_tree(self):
        tree = BinaryTree()
        tree.root = self.get_node(self.E, tree.root)
        tree.root.parent = None
        level = [tree.root]

        while level:
            next_level = list()
            for n in level:
                if n.left:
                    n.left.parent = n
                    next_level.append(n.left)
                if n.right:
                    n.right.parent = n
                    next_level.append(n.right)
                level = next_level
        return tree

    """
        Obtém o nodo derivado do atual de forma recursiva
        A formação de cada nodo é dependente do tipo de operador
    """
    def get_node(self, current, parent):
        node = Node()
        #node.parent = parent
        if self.is_dictionary(current):
            node.value = self.get_operator(current)
            if node.value == "|":
                node.left = self.get_node(list(current.values())[0][0], node)
                if len(list(current.values())[0]) == 2:
                    node.right = self.get_node(list(current.values())[0][1], node)
                else:
                    del list(current.values())[0][0]
                    node.right = self.get_node(current, node)

            else:
                node.left = self.get_node(list(current.values())[0], node)
        elif len(current) > 1:
            node.value = "."
            node.left = self.get_node(current[0], node)
            if len(current) == 2:
                node.right = self.get_node(current[1], node)
            elif len(current) > 2:
                node.right = self.get_node(current[1:], node)
        else:
            if self.is_dictionary(current[0]):
                node = self.get_node(current[0], node)
            else:
                node.value = current[0]
        return node


    """
        Verifica se o próximo símbolo é um dicionário,
        o que significa que o nodo atual é '*' ou '?'
    """
    def is_dictionary(self, c):
        return type(c) is dict

    """
        Retorna o operador atual
    """
    def get_operator(self, c):
        if self.is_dictionary(c):
            return list(c.keys())[0]

    """
        Função auxiliar que imprime na tela a árvore binária
    """
    def print_tree(self, tree):
        root = tree.root
        level = [root]
        while level:
            x = ' '
            for node in level:
                str_is_double_parent = "  "
                if node.parent:
                    if node.parent.value in ('.','|'):
                        str_is_double_parent = "  "
                x += "("+str(node.value) + ")"+str_is_double_parent
            print(x)

            next_level = list()
            for n in level:
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
                level = next_level

    """
        Função auxiliar que imprime na tela a árvore binária costurada
        indicando o número do nodo folha
    """
    def print_threaded_tree(self, tree):
        root = tree.root
        level = [root]
        while level:
            x = ' '
            for node in level:
                thread = " "
                leaf_num = " "
                if node in tree.leafs:
                    leaf_num = str(tree.leafs[node])
                if node.thread:
                    x += leaf_num+"("+str(node.value) + ")-->("+str(node.thread.value)+")   "
                else:
                    x += leaf_num+"("+str(node.value) + ")         "
            print(x)
            next_level = list()
            for n in level:
                if n.left:
                    next_level.append(n.left)
                if n.right:
                    next_level.append(n.right)
                level = next_level

    """
        Retorna o nodo folha mais a esquerda da árvore
    """
    def get_most_left_node(self, tree):
        current = tree.root
        while current.left != None:
            current = current.left
        return current

    """
        Insere uma costura do nodo atual até o nodo pai livre mais próximo
    """
    def thread(self, node):
        current = node
        if current.parent:
            while current.parent:
                current = current.parent
                if current == None:
                    break
                if current.is_threaded == False:
                    node.thread = current
                    current.is_threaded = True
                    break
        if node.thread == None:
            node.thread = Node("k") # O nodo 'k' representa o símbolo no algoritmo

    """
        Inicializa costura da árvore
    """
    def fill_threaded_tree(self,tree):
        initial_node = self.get_most_left_node(tree)
        if self.is_leaf(initial_node):
            self.append_leaf_enum(initial_node, tree)
            tree.sigma.add(initial_node.value)
        current = initial_node
        self.thread(current)
        visited = list()
        visited.append(current)
        current = current.parent
        visited.append(current)
        self.explore_for_thread(current, visited, tree)

    """
        Identifica nodos folha
    """
    def append_leaf_enum(self, node, tree):
        index = len(tree.leafs) + 1
        tree.leafs[node] = index
        node.id = index


    """
        Explora a árvore para completar as costuras nos nodos corretos
    """
    def explore_for_thread(self, current, visited, tree):
        if current:
            if current.value in (".", "|"):
                left_child = current.left
                if left_child not in visited:
                    visited.append(left_child)
                    self.explore_for_thread(left_child, visited, tree)
                right_child = current.right
                if right_child not in visited:
                    visited.append(right_child)
                    self.explore_for_thread(right_child, visited, tree)
                current = current.parent
                if current not in visited:
                    visited.append(current)
                    self.explore_for_thread(current, visited, tree)
            else:
                self.thread(current)
                if self.is_leaf(current):
                    self.append_leaf_enum(current, tree)
                    tree.sigma.add(current.value)
                if current.left not in visited:
                    c = current.left
                    visited.append(c)
                    self.explore_for_thread(c, visited, tree)
                current = current.parent
                if current not in visited:
                    visited.append(current)
                    self.explore_for_thread(current, visited, tree)

    """
        Retorna se o nodo de entrada é folha
    """
    def is_leaf(self, node):
        return not node.left

    """
        A partir do nodo raiz, utilizado rotinas subir/descer do algoritmo
        De Simone, preenche os estados alcançáveis e cria uma composição

        Então retorna o automato equivalente
    """
    def fill_composing_and_get_automata(self, tree):
        current = tree.root
        first_state_name = self.add_composing_state(tree)
        self.tree_move_down(current, first_state_name, tree)
        new_states = []
        sigma = sorted(tree.sigma)

        automata = FiniteAutomata()
        automata.sigma = sigma
        automata.initial_state = first_state_name
        automata.is_deterministic = True
        automata.transitions[first_state_name] = {}


        for symbol in sigma:
            state_name = self.add_composing_state(tree)
            new_states.append(state_name)
            for node in tree.composing_states[first_state_name]:
                if node.value == symbol:
                    self.tree_move_up(node, state_name, tree)
            automata.transitions[first_state_name][symbol] = state_name


        while len(new_states) > 0:
            states = new_states
            for state in states:
                automata.transitions[state] = {}
            new_states = []
            for symbol in sigma:
                for state in states:
                    state_name = self.add_composing_state(tree)
                    automata.transitions[state][symbol] = state_name
                    for node in tree.composing_states[state]:
                        if node.value == symbol:
                            self.tree_move_up(node, state_name, tree)
                    state_result = tree.composing_states[state_name]
                    if (list(tree.composing_states.values()).count(state_result) > 1):
                        del tree.composing_states[state_name]
                        for key, value in list(tree.composing_states.items()):
                            if value == state_result:
                                automata.transitions[state][symbol] = key
                                break
                    else:
                        new_states.append(state_name)

        for state in tree.composing_states:
            automata.K.append(state)
            automata.states[state] = state
            for node in tree.composing_states[state]:
                if node.value == "k":
                    automata.final_states.append(state)
        return automata


    """
        Para cada estado adicionado, é utilizado para verificar se não
        existe no conjunto atual de estados, outro equivalente.
    """
    def is_new_state_equivalent(self, state, tree):
        for state in sorted(tree.composing_states):
            return state == tree.composing_states[state]



    """
        Algoritmo De Simone: Rotinas descer
        Criando um estado de composição
    """
    def tree_move_down(self, current, state_name, tree):
        if current.value in ("|", ".", "?", "*"):
            left_child = current.left
            self.tree_move_down(left_child, state_name, tree)
            if current.value == "|":
                right_child = current.right
                self.tree_move_down(right_child, state_name, tree)
            if current.value in ("?", "*"):
                thread = current.thread
                self.tree_move_up(thread, state_name, tree)
        else: # Leaf
            self.add_leaf_to_composing(current, state_name, tree)


    """
        Algoritmo De Simone: Rotinas subir
        Criando um estado de composição
    """
    def tree_move_up(self, current, state_name, tree):
        if current.value == ".":
            right_child = current.right
            self.tree_move_down(right_child, state_name, tree)
        elif current.value == "|":
            right_child = current.right
            while not right_child.thread:
                right_child = right_child.right
            self.tree_move_up(right_child.thread, state_name, tree)
        elif current.value == "?":
            thread = current.thread
            self.tree_move_up(thread, state_name, tree)
        elif current.value == "*":
            left_child = current.left
            self.tree_move_down(left_child, state_name, tree)
            thread = current.thread
            self.tree_move_up(thread, state_name, tree)
        else: # Leaf
            if current.value == "k":
                self.add_leaf_to_composing(current, state_name, tree)
            else:
                self.tree_move_up(current.thread, state_name, tree)


    """
        Algoritmo De Simone:
        Adiciona estado de composição
    """
    def add_composing_state(self, tree):
        states = tree.composing_states
        new_state_name = self.get_next_state_name(states)
        tree.composing_states[new_state_name] = []
        return new_state_name

    """
        Algoritmo De Simone:
        Adiciona nodo folha ao estado de composição se
        o mesmo já não está presente

    """
    def add_leaf_to_composing(self, leaf, state_name, tree):
        if leaf not in tree.composing_states[state_name]:
            tree.composing_states[state_name].append(leaf)

    """
        Função auxiliar que imprime os estados de composição
    """
    def print_composing(self, tree):
        print("Composing")
        x = ""
        for state in sorted(tree.composing_states):
            x += str(state) + ": "
            for node in tree.composing_states[state]:
                id = node.id
                if not id:
                    id = ""
                x+= str(id)+"_"+node.value + " | "
            print(x)
            x = ""

    """
        Função auxilar para retornar o nome de um próximo estado
        no formato padrão da aplicação
    """
    def get_next_state_name(self, states):
        return "q"+str(len(states))
