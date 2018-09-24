#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_uppercase

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
        if A not in self.G:
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
        if A in self.G:
            del self.G[A]

    """
        Remove uma regra de produção A -> B
    """
    def remove_rule(self, A, B):
        if A in self.G:
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
        print((self.initial_state))
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
        print((self.G))

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
            for production in list(g.G.keys()):
                if production != g.initial_state:
                    rules = ""
                    for rule in g.G[production]:
                        rules += str(rule) + " | "
                    rules = rules[0:-3]
                    lines += (str(production) + " --> " + rules + "\n")
            lines += "}"

        return lines
