#!/usr/bin/env python # -*- coding: utf-8 -*
from binary_tree import *
from string import ascii_uppercase
import copy


class RegGram:
    def  __init__(self, G={}, initial_state=None):
        self.G = G
        self.initial_state = initial_state


    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

    def is_initial_state(self, state):
        return state == self.initial_state


    # Productions A -> B
    def add_production(self, A):
        if not self.G:
            self.initial_state = A
        if not self.G.has_key(A):
            if self.validate_production(A):
                self.G[A] = []
                return True
            else:
                return str(A) + " --> is not a valid production for Regular Grammars"
        return True

    # Rules B on A -> B
    def add_rule(self, A, B):
        if self.add_production(A) == True:
            if B not in self.G[A]:
                if self.validate_rule(B):
                    if self.validate_epsilon(B):
                        self.G[A].append(B)
                        return True
                    else:
                        return "The initial state can't be assigned on the right side of the production because its production has epsilon(&)"
                elif B == "&":
                    if self.is_initial_state(A):
                        if not self.has_initial_state_on_right_side():
                            self.G[A].append(B)
                            return True
                        else:
                            return "& cant be assigned because the initial state is on a right side production"

                    else:
                        return "& can only be assigned to the initial state"

                else:
                    return " --> " +str(B) + " is not a valid production for Regular Grammars"
        else:
            return self.add_production(A)

    def validate_production(self, A):
        return ((len(A) == 1) and (A[0].isupper()))

    def validate_rule(self, B):
        if (len(B) == 1) and (B[0].islower() or B[0].isdigit()):
            return True
        elif (len(B) == 2) and (B[0].islower() or B[0].isdigit()) and (B[1].isupper()):
            self.add_production(B[1])
            return True
        return False

    def validate_epsilon(self, B):
        if len(B) > 1:
            if B[1] == self.initial_state:
                if "&" in self.G[self.initial_state]:
                    return False
        return True

    def has_initial_state_on_right_side(self):
        for production in self.G:
            for B in self.G[production]:
                if len(B) > 1:
                    if B[1] == self.initial_state:
                        return True
        return False


    def remove_production(self, A):
        if self.G.has_key(A):
            del self.G[A]

    def remove_rule(self, A, B):
        if self.G.has_key(A):
            if B in self.G[A]:
                self.G[A].remove(B)

    def validate_grammar(self):
        for prod in self.G:
            if not self.G[prod]:
                return False
        return True

    def is_lower(self, B):
        return B.islower()


    def check_input(self, input):
        return input in self.generate_sentences(len(input))

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
        Returns a Dict with terminal/non-terminal symbols
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

    def get_vn(self):
        return self.get_info()["vn"]

    def get_vt(self):
        return self.get_info()["vt"]

    """
        Returns the equivalent finite automata
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
            fa.states[k] = k
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
    Class Regex
"""
class Regex:
    def  __init__(self):
        self.literal = ""
        self.E = []

    """
        Transforms a string input into a array of symbols

        - Operations '|', '?', '*' and '+' are represented as a dictionary
        - Concatenations are represented by array's symbols
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
            elif char in ("*", "?", "+"):
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
        Converts Regular Expression -> Finite Automata
        Using De Simone's Method
    """
    def get_equivalent_automata(self):
        tree = self.get_tree()
        self.fill_threaded_tree(tree)
        # self.print_threaded_tree(tree)
        fa = self.fill_composing_and_get_automata(tree)
        # self.print_composing(tree)
        return fa

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
        Checks if the next symbol is an dictionary,
        which means that the current node is a '*', '+' or '?'
    """
    def is_dictionary(self, c):
        return type(c) is dict

    """
        Returns the current operator ('*', '+' or '?')
    """
    def get_operator(self, c):
        if self.is_dictionary(c):
            return c.keys()[0]

    """
        Prints the Binary Tree improving interpretability
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

    def get_most_left_node(self, tree):
        current = tree.root
        while current.left != None:
            current = current.left
        return current

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
            node.thread = Node("k")

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


    def append_leaf_enum(self, node, tree):
        index = len(tree.leafs) + 1
        tree.leafs[node] = index
        node.id = index


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

    def is_leaf(self, node):
        return not node.left

    def fill_composing_and_get_automata(self, tree):
        current = tree.root
        first_state_name = self.add_composing_state(tree)
        self.tree_move_down(current, first_state_name, tree)
        new_states = []
        sigma = sorted(tree.sigma)

        automata = FiniteAutomata()
        automata.sigma = sigma
        automata.initial_state = first_state_name
        automata.deterministic = True
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
            for node in tree.composing_states[state]:
                if node.value == "k":
                    automata.final_states.append(state)
        return automata


    def is_new_state_equivalent(self, state, tree):
        for state in sorted(tree.composing_states):
            return state == tree.composing_states[state]



    """
        De Simone's Algorithm - Down routine
        Compose a composing state
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

    def add_composing_state(self, tree):
        states = tree.composing_states
        new_state_name = self.get_next_state_name(states)
        tree.composing_states[new_state_name] = []
        return new_state_name

    def add_leaf_to_composing(self, leaf, state_name, tree):
        if leaf not in tree.composing_states[state_name]:
            tree.composing_states[state_name].append(leaf)

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


    def get_next_state_name(self, states):
        return "q"+str(len(states))




class FiniteAutomata:
    def  __init__(self):
        self.K = []
        self.states = {} # To use when states were renamed
        self.deterministic = False
        self.sigma = []
        self.transitions = {}
        self.initial_state = None
        self.final_states = []

    """
        Returns an deterministic version of the finite automata
    """
    def get_deterministic(self):
        dfa = FiniteAutomata()
        dfa.sigma = self.sigma[:]
        # K' = {p(k)}
        dfa.K.append([self.initial_state])
        for symbol in self.K:
            for s in self.sigma:
                state = self.transitions[symbol][s]
                if state not in dfa.K:
                    dfa.K.append(state)
        print "dfa.K"
        print dfa.K


        possible_states = ascii_uppercase[:18]+ascii_uppercase[19:] # avoid "S"
        # Rename states
        for i, state in enumerate(dfa.K):
            if i == 0:
                dfa.states["S"] = state
            else:
                dfa.states[possible_states[i-1]] = state

        print "dfa.states"
        print dfa.states

        # qo' = [qo]
        dfa.initial_state = "S"

        # F' = {p(K) | p(K) intersecction with F != empty state}
        for state in dfa.states:
            for s in dfa.states[state]:
                if s in self.final_states:
                    dfa.final_states.append(state)
        print "dfa.final_states"
        print dfa.final_states

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
                    if  (
                        (dfa.transitions[state][item] not in dfa.K)
                        and
                        (dfa.transitions[state][item] not in new_states)
                        ):
                        new_states.append(dfa.transitions[state][item])

            for state in new_states:
                dfa.K.append(state)
                new_state_name = possible_states[len(dfa.states)]
                dfa.states[new_state_name] = state

        print "dfa.transitions"
        print dfa.transitions
        dfa.deterministic = True
        dfa.K = dfa.states
        return dfa

    def get_minimized(self):
        pass

    """
        Returns an equivalent Regular Grammar
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
                    rg.G[state].append(key+value)
        print "\n\n\nself.K:"
        print self.K
        if self.deterministic:
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


    def get_name_of_state(self, transition):
        for state in self.states.keys():
            if self.states[state] == transition:
                return state


    """
        Prints the finite automata as a table to improve interpretability
    """
    def pretty_print(self):
        print "Finite Automata:\n"
        bigger = self.get_max_column_size() * 5
        descript = []
        descript.append("        |")
        hr = "-----------"
        symbols = []
        for symbol in self.sigma:
            if symbol not in symbols:
                symbols.append(symbol)
                if self.deterministic:
                    descript[0] += ""+ str(symbol) + self.print_spaces(2) + "|"
                else:
                    descript[0] += "   "+ str(symbol) + self.print_spaces(bigger - 5) + " |"
                hr += "----------"

        str_final = " "
        if self.initial_state in self.final_states:
            str_final = "*"
        descript.append(str_final + "->" + str(self.initial_state) + "   |")
        for symbol in symbols:
            size = len(self.transitions[self.initial_state][symbol])
            if self.deterministic:
                #descript[1] += "" + str(self.get_name_of_state(self.transitions[self.initial_state][symbol])) + self.print_spaces(1)+ "|"
                descript[1] += "" + str(self.transitions[self.initial_state][symbol]) + self.print_spaces(1)+ "|"
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
                        if self.deterministic:
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
        return pretty


    """
        Returns the size of the max column to improve pretty print
    """
    def get_max_column_size(self):
        max = 0
        for symbol in self.K:
            if self.deterministic:
                return 2
            for rule in self.transitions[symbol]:
                size = len(self.transitions[symbol][rule])
                if size > max:
                    max = size
        return max

    """
        Prints 'n' blank spaces
    """
    def print_spaces(self, n):
        s = ""
        for _ in range(n):
            s += " "
        return s

    def symbols_to_alphabet(self):
        for state in self.states:
            print state
