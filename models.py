#!/usr/bin/env python # -*- coding: utf-8 -*
from binary_tree import *
from string import ascii_uppercase
import copy


"""
    Classe que representa as Gramáticas Regulares
"""
class RegGram:
    def  __init__(self, G={}, initial_state=None):
        self.G = G
        self.initial_state = initial_state


    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

    def is_initial_state(self, state):
        return state == self.initial_state


    """
        Adiciona produção, se válida, à gramática regular.
        A primeira produção inserida será o estado inicial da GR
        G: P =  {
                    A ->
                }
    """
    def add_production(self, A):
        if not self.G:
            self.initial_state = A
        if not self.G.has_key(A):
            if self.validate_production(A):
                self.G[A] = []
                return True
            else:
                return str(A) + " --> não é uma produção válida para Gramáticas Regulares"
        return True

    """
        Adiciona regra de produção, se válida, à gramática regular.

        Somente são válidas regras do tipo: Vt (ex: a) ou VtVn (ex: aA)

        Verifica se epsilon pode ser inserido e se for, analisa próximas
        inserções para evitar o estado inicial do lado direito das produções

        G: P =  {
                    A -> B
                }
    """
    def add_rule(self, A, B):
        if self.add_production(A) == True:
            if B not in self.G[A]:
                if self.validate_rule(B):
                    if self.validate_epsilon(B):
                        self.G[A].append(B)
                        return True
                    else:
                        return "O estado inicial não pode ser adicionado no lado direito da produção pois o mesmo contém epsilon transição"
                elif B == "&":
                    if self.is_initial_state(A):
                        if not self.has_initial_state_on_right_side():
                            self.G[A].append(B)
                            return True
                        else:
                            return "& não pode ser adicionado pois o estado inicial está presente do lado direito de alguma produção"

                    else:
                        return "& só pode ser adicionado ao estado inicial " + self.initial_state

                else:
                    return " --> " +str(B) + " não é uma produção válida para Gramáticas Regulares"
        else:
            return self.add_production(A)

    """
        Valida formato de produções
    """
    def validate_production(self, A):
        return ((len(A) == 1) and (A[0].isupper()))

    """
        Valida formato das regras de produção
    """
    def validate_rule(self, B):
        if (len(B) == 1) and (B[0].islower() or B[0].isdigit()):
            return True
        elif (len(B) == 2) and (B[0].islower() or B[0].isdigit()) and (B[1].isupper()):
            self.add_production(B[1])
            return True
        return False

    """
        Valida inserção de epsilon
    """
    def validate_epsilon(self, B):
        if len(B) > 1:
            if B[1] == self.initial_state:
                if "&" in self.G[self.initial_state]:
                    return False
        return True

    """
        Verifica a existência de estado inicial no lado direito das produções
    """
    def has_initial_state_on_right_side(self):
        for production in self.G:
            for B in self.G[production]:
                if len(B) > 1:
                    if B[1] == self.initial_state:
                        return True
        return False

    """
        Remove uma produção A
    """
    def remove_production(self, A):
        if self.G.has_key(A):
            del self.G[A]

    """
        Remove uma regra de produção A -> B
    """
    def remove_rule(self, A, B):
        if self.G.has_key(A):
            if B in self.G[A]:
                self.G[A].remove(B)

    """
        Valida existência de pelo menos uma produção
    """
    def validate_grammar(self):
        for prod in self.G:
            if not self.G[prod]:
                return False
        return True

    """
        Verifica se B é Vt
    """
    def is_lower(self, B):
        return B.islower()

    """
        Verifica se sentença pertence à gramática
    """
    def check_input(self, input):
        return input in self.generate_sentences(len(input))

    """
        Gera possíveis sentenças de tamanho 'size'
    """
    def generate_sentences(self, size):
        state = self.initial_state
        final_sentences = []
        sentences = []
        for seq in self.G[state]:
            if self.is_lower(seq):
                final_sentences.append(seq)
            else:
                sentences.append(seq)

        size -= 1
        while(size > 0):
            size -= 1
            tmp_sentences = sentences[:]
            for seq in tmp_sentences:
                for new_seq in self.G[seq[-1]]:
                    new_seq = seq[0:-1] + new_seq
                    if self.is_lower(new_seq):
                        final_sentences.append(new_seq)
                    else:
                        sentences.append(new_seq)
        return final_sentences

    """
        De forma otimizada, verifica se sentença pertence à gramática
        utilizando caminhos férteis para a sentença.
    """
    def check_input_optimized(self, input):
        size = len(input)
        state = self.initial_state
        final_sentences = []
        sentences = []
        print self.initial_state
        for seq in self.G[state]:
            if self.is_lower(seq):
                if (len(seq) == len(input)):
                    final_sentences.append(seq)
            elif (seq[0] == input[0]):
                sentences.append(seq)
        size -= 1
        i = 1
        while(size > 0):
            size -= 1
            tmp_sentences = sentences[:]
            sentences = []
            for seq in tmp_sentences:
                for new_seq in self.G[seq[-1]]:
                    new_seq = seq[0:-1] + new_seq
                    if self.is_lower(new_seq):
                        if (len(new_seq) == len(input)):
                            final_sentences.append(new_seq)
                    elif (new_seq[i] == input[i]):
                        sentences.append(new_seq)
            i += 1
        return (input in final_sentences)

    # Prints the Grammar
    def show(self):
        print self.G

    """
        Retorna um dicionário com símbolos terminais e não terminais
    """
    def get_info(self):
        vn = [self.initial_state]
        vt = []
        for state in self.G:
            if state not in vn:
                vn.append(state)
            for rule in self.G[state]:
                for char in rule:
                    if char.islower() and (char not in vt):
                        vt.append(char)
        return {"vn": vn, "vt": vt}

    """
        Retorna uma lista de símbolos não terminais
    """
    def get_vn(self):
        return self.get_info()["vn"]

    """
        Retorna uma lista de símbolos terminais
    """
    def get_vt(self):
        return self.get_info()["vt"]

    """
        Retorna um autômato finito equivalente à gramatica regular
    """
    def get_eq_automata(self):
        fa = FiniteAutomata()
        new_symbol = None
        for c in ascii_uppercase:
            if c not in self.get_vn():
                new_symbol = c
                break
        vn = self.get_vn()
        vn.append(new_symbol)
        fa.K = vn
        for k in fa.K:
            fa.states[k] = [k]
        fa.sigma = self.get_vt()
        fa.initial_state = self.initial_state
        fa.final_states.append(new_symbol)
        if "&" in self.G[self.initial_state]:
            fa.final_states.append(fa.initial_state)

        for symbol in self.get_vn():
            fa.transitions[symbol] = {}
            for rule in self.get_vt():
                if rule in self.G[symbol]:
                    fa.transitions[symbol][rule] = [new_symbol]
                else:
                    fa.transitions[symbol][rule] = ["-"]
            for rule in self.G[symbol]:
                if len(rule) == 2:
                    if (fa.transitions[symbol][rule[0]] and fa.transitions[symbol][rule[0]] != ["-"]):
                        fa.transitions[symbol][rule[0]].append(rule[1])
                    else:
                        fa.transitions[symbol][rule[0]] = [rule[1]]
        fa.transitions[new_symbol] = {}
        for rule in fa.sigma:
            fa.transitions[new_symbol][rule] = ["-"]
        return fa

    """
        Função auxiliar que permite melhor visualização da gramática regular
    """
    def get_pretty(g):
        lines = ""
        if g.initial_state != None:
            lines = "G: P = {\n"
            rules = ""
            for rule in g.G[g.initial_state]:
                rules += str(rule) + " | "
            rules = rules[0:-3]
            lines += (str(g.initial_state) + " --> " + rules + "\n")
            for production in g.G.keys():
                if production != g.initial_state:
                    rules = ""
                    for rule in g.G[production]:
                        rules += str(rule) + " | "
                    rules = rules[0:-3]
                    lines += (str(production) + " --> " + rules + "\n")
            lines += "}"

        return lines

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
                node.left = self.get_node(current.values()[0][0], node)
                if len(current.values()[0]) == 2:
                    node.right = self.get_node(current.values()[0][1], node)
                else:
                    del current.values()[0][0]
                    node.right = self.get_node(current, node)

            else:
                node.left = self.get_node(current.values()[0], node)
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
            return c.keys()[0]

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
            print x

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
            print x
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
                    if (tree.composing_states.values().count(state_result) > 1):
                        del tree.composing_states[state_name]
                        for key, value in tree.composing_states.items():
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
        print "Composing"
        x = ""
        for state in sorted(tree.composing_states):
            x += str(state) + ": "
            for node in tree.composing_states[state]:
                id = node.id
                if not id:
                    id = ""
                x+= str(id)+"_"+node.value + " | "
            print x
            x = ""

    """
        Função auxilar para retornar o nome de um próximo estado
        no formato padrão da aplicação
    """
    def get_next_state_name(self, states):
        return "q"+str(len(states))



"""
    Classe que representa Autômatos Finitos
"""

class FiniteAutomata:
    def  __init__(self):
        self.K = []
        self.states = {} # To use when states were renamed
        self.is_deterministic = False
        self.sigma = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []

    """
        Retorna uma versão deterministica do autômato finito
    """

    def get_deterministic(self):
        if self.is_deterministic:
            return copy.copy(self)
        dfa = FiniteAutomata()
        dfa.sigma = self.sigma[:]
        # K' = {p(k)}
        dfa.K.append([self.initial_state])
        for symbol in self.K:
            for s in self.sigma:
                state = self.transitions[symbol][s]
                if state not in dfa.K:
                    dfa.K.append(state)
        # Rename states
        for i, state in enumerate(dfa.K):
            dfa.states["q"+str(i)] = state

        # qo' = [qo]
        dfa.initial_state = "q0"

        # transitions
        new_states = None
        while new_states != []:
            new_states = []
            for state in dfa.states:
                dfa.transitions[state] = {}
                for item in dfa.sigma:
                    tmp = []
                    for s in dfa.states[state]:
                        if s != '-':
                            for transition in self.transitions[s][item]:
                                if transition not in tmp:
                                    tmp.append(transition)
                                    dfa.transitions[state][item] = tmp
                        else:
                            dfa.transitions[state][item] = '-'
                    if len(dfa.transitions[state][item]) > 1 and ('-' in dfa.transitions[state][item]):
                        dfa.transitions[state][item].remove('-')
                    if  (
                        (dfa.transitions[state][item] not in dfa.K)
                        and
                        (dfa.transitions[state][item] not in new_states)
                        ):
                        new_states.append(dfa.transitions[state][item])

            index = len(dfa.states)
            for state in new_states:
                dfa.K.append(state)
                new_state_name = "q"+str(index)
                index += 1
                dfa.states[new_state_name] = state

        for state in dfa.transitions:
            for symbol in dfa.sigma:
                value = dfa.transitions[state][symbol]
                dfa.transitions[state][symbol] = self.get_state_name(dfa, value)

        dfa.is_deterministic = True
        dfa.K = dfa.transitions.keys()

        # F' = {p(K) | p(K) intersecction with F != empty state}
        for state in dfa.states:
            for s in dfa.states[state]:
                if s in self.final_states:
                    dfa.final_states.append(state)
        return dfa

    """
        Procura nos estados do novo autômato o nome equivalente aos
        estados compostos do autômato original
    """
    def get_state_name(self, dfa, search_value):
        for key, value in dfa.states.items():
            if value == search_value:
                return key

    """
        Retorna o autômato finito mínimo (único)
        A autômato de entrada deve ser deterministico

        - Remove estados inalcançáveis
        - Remove estados mortos
        - Adiciona um estado de erro (indefinido)
        - Agrupa estados em classes de equivalência
    """
    def get_minimized(self):
        if not self.is_deterministic:
            return "Error, minimization requires a deterministic finite automata"
        minimized_dfa = copy.copy(self)

        minimized_dfa.remove_unreachable_states()
        minimized_dfa.remove_dead_states()
        minimized_dfa.add_undefined_state()
        minimized_dfa = minimized_dfa.group_equivalent_classes()

        return minimized_dfa

    """
        - Remove estados inalcançáveis
    """
    def remove_unreachable_states(self):
        reachable = [self.initial_state]
        new_reachable_states = [self.initial_state]
        while new_reachable_states != []:
            current_state = new_reachable_states[0]
            del new_reachable_states[0]
            for symbol in self.sigma:
                new_state = self.transitions[current_state][symbol]
                if new_state not in reachable:
                    reachable.append(new_state)
                    if new_state not in new_reachable_states:
                        new_reachable_states.append(new_state)
        for transition in self.transitions.keys():
            if transition not in reachable:
                del self.transitions[transition]
                del self.states[transition]
                self.K.remove(transition)
                if transition in self.final_states:
                    self.final_states.remove(transition)
        for state in self.transitions:
            for symbol in self.sigma:
                if self.transitions[state][symbol] not in self.K:
                    self.transitions[state][symbol] = "-"

    """
        - Remove estados mortos
    """
    def remove_dead_states(self):
        alive = self.final_states[:]
        new_alive_states = None
        while new_alive_states != []:
            new_alive_states = []
            for state in self.transitions:
                for symbol in self.sigma:
                    transition = self.transitions[state][symbol]
                    if transition in alive:
                        if state not in alive:
                            alive.append(state)
                            if state not in new_alive_states:
                                new_alive_states.append(state)
                            break
        for transition in self.transitions.keys():
            if transition not in alive:
                del self.transitions[transition]
                del self.states[transition]
                self.K.remove(transition)
                if transition in self.final_states:
                    self.final_states.remove(transition)
        for state in self.transitions:
            for symbol in self.sigma:
                if self.transitions[state][symbol] not in self.K:
                    self.transitions[state][symbol] = "-"

    """
        - Adiciona um estado de erro (indefinido)
    """
    def add_undefined_state(self):
        self.K.append("qE")
        self.states["qE"] = ["qE"]
        self.transitions["qE"] = {}
        for symbol in self.sigma:
            self.transitions["qE"][symbol] = "qE"

        for state in self.transitions:
            for symbol in self.sigma:
                if self.transitions[state][symbol] == "-":
                    self.transitions[state][symbol] = "qE"

    """
        Cria classes de equivalência entre estados finais e não finais,
        resultando em um autômato mínimo equivalente ao original
    """
    def group_equivalent_classes(self):
        final_states = self.final_states[:]
        non_final_states = ([state for state in self.K[:]
                            if state not in final_states])
        equivalent_classes = {0: final_states, 1: non_final_states}
        last_equivalent_classes = equivalent_classes
        while True:
            combinations = {}
            new_equivalent_classes = {}
            for state in sorted(self.K):
                is_state_final = state in final_states
                not_found = True
                next_combination = {}
                transition = {}
                for symbol in self.sigma:
                    transition[symbol] = self.transitions[state][symbol]
                    next_combination[symbol] = self.get_equivalent_class_of_state(transition[symbol], last_equivalent_classes)

                if next_combination in combinations.values():
                    for c in combinations:
                        if next_combination == combinations[c]:
                            if state not in new_equivalent_classes[c]:
                                both_final = new_equivalent_classes[c][0] in final_states and is_state_final
                                both_non_final = new_equivalent_classes[c][0] in non_final_states and not is_state_final
                                if both_final or both_non_final:
                                    new_equivalent_classes[c].append(state)
                                    not_found = False
                            break
                if not_found:
                    index = len(combinations)
                    combinations[index] = next_combination
                    new_equivalent_classes[index] = []
                    if state not in new_equivalent_classes[index]:
                        new_equivalent_classes[index].append(state)

            if new_equivalent_classes == last_equivalent_classes:
                break
            last_equivalent_classes = new_equivalent_classes


        final_classes = {}
        for eq_class in last_equivalent_classes:
            final_classes["q"+str(eq_class)] = last_equivalent_classes[eq_class]

        final_transitions = {}
        for eq_class in final_classes:
            transition = {}
            for symbol in self.sigma:
                t = self.transitions[final_classes[eq_class][0]][symbol]
                state = self.get_equivalent_class_of_state(t, final_classes)
                transition[symbol] = state
            final_transitions[eq_class] = transition

        new_fa = FiniteAutomata()

        for eq_class in final_classes:
            new_fa.states[eq_class] = final_classes[eq_class]
        new_fa.K = new_fa.states.keys()
        new_fa.is_deterministic = True
        new_fa.sigma = self.sigma
        for eq_class, states in new_fa.states.items():
            if self.initial_state in states:
                new_fa.initial_state = eq_class

        new_fa.transitions = final_transitions

        new_fa.final_states = []
        for state in new_fa.states:
            if new_fa.states[state][0] in self.final_states:
                new_fa.final_states.append(state)

        return new_fa


    """
        Para a iteração atual, busca a classe de equivalência na qual
        um estado 'state' é pertencente
    """
    def get_equivalent_class_of_state(self, state, equivalent_classes):
        for key in equivalent_classes:
            if state in equivalent_classes[key]:
                return key


    """
        Retorna uma gramática regular equivalente ao autômato finito
    """
    def get_eq_reg_gram(self):
        rg = RegGram()
        rg.initial_state = self.initial_state
        state = self.initial_state
        rg.G[state] = []
        for key in self.transitions[state]:
            for value in self.transitions[state][key]:
                if value in self.final_states:
                    rg.G[state].append(key)
                else:
                    rg.G[state].append(key+value) # TODO: VERIFICAR ISSO NO DETERMINISTICO
        if self.is_deterministic:
            for state in self.states:
                rg.G[state] = []
                for key in self.transitions[state]:
                    for value in self.transitions[state][key]:
                        if value in self.final_states:
                            rg.G[state].append(key)
                        else:
                            rg.G[state].append(key+value)
        else:
            for state in self.K:
                rg.G[state] = []
                for key in self.transitions[state]:
                    for value in self.transitions[state][key]:
                        if value in self.final_states:
                            rg.G[state].append(key)
                        else:
                            rg.G[state].append(key+value)
        if self.initial_state in self.final_states:
            rg.G[rg.initial_state].append("&")
        return rg

    """
        Retorna nome do estado dado a composição de estados originais,
        antes da determinização
    """
    def get_name_of_state(self, transition):
        for state in self.states.keys():
            if self.states[state] == transition:
                return state


    """
        Imprime o autômato finito através de uma tabela para aumentar
        a interpretabilide.
    """
    def pretty_print(self):
        bigger = self.get_max_column_size() * 5
        descript = []
        descript.append("        |")
        hr = "---------"
        symbols = []
        for symbol in sorted(self.sigma):
            if symbol not in symbols:
                symbols.append(symbol)
                if self.is_deterministic:
                    descript[0] += ""+ str(symbol) + self.print_spaces(2) + "|"
                else:
                    descript[0] += "   "+ str(symbol) + self.print_spaces(bigger - 5) + " |"
                hr += "----"

        str_final = " "
        if self.initial_state in self.final_states:
            str_final = "*"
        descript.append(str_final + "->" + str(self.initial_state) + "   |")
        for symbol in symbols:
            size = len(self.transitions[self.initial_state][symbol])
            if self.is_deterministic:
                descript[1] += "" + str(self.transitions[self.initial_state][symbol]) + " |"
            else:
                descript[1] += "" + str(self.transitions[self.initial_state][symbol]) + self.print_spaces(bigger - size * 5)+ "|"

        i = 2
        for state in self.transitions:
            if state != self.initial_state:
                str_final = "   "
                if state in self.final_states:
                    str_final = " * "
                descript.append(str_final + state + "   |")
                for symbol in symbols:
                    if symbol in self.transitions[state]:
                        size = len(self.transitions[state][symbol])
                        if self.is_deterministic:
                            #descript[i] += "" + str(self.get_name_of_state(self.transitions[state][symbol])) + self.print_spaces(1) + "|"
                            descript[i] += "" + str(self.transitions[state][symbol]) + self.print_spaces(1) + "|"
                        else:
                            descript[i] += "" + str(self.transitions[state][symbol]) + self.print_spaces(bigger - size * 5) + "|"
                    else:
                        descript[i] += "" + "----" + " |"
                i += 1


        pretty = descript[0]+"\n"+hr+"\n"
        for line in descript[1:]:
            pretty += line + "\n"
        pretty += hr

        print pretty
        #return pretty


    """
        Função auxiliar para impressão da tabela que representa o AF
    """
    def get_max_column_size(self):
        max = 0
        for symbol in self.K:
            if self.is_deterministic:
                return 2
            for rule in self.transitions[symbol]:
                size = len(self.transitions[symbol][rule])
                if size > max:
                    max = size
        return max

    """
        Função auxiliar para impressão de espaços em branco para
        alinhamento da impressão do AF
    """
    def print_spaces(self, n):
        s = ""
        for _ in range(n):
            s += " "
        return s
