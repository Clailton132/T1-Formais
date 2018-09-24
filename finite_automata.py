#!/usr/bin/env python
# -*- coding: utf-8 -*-

from string import ascii_uppercase
import copy

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
        dfa.K = list(dfa.transitions.keys())

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
        for key, value in list(dfa.states.items()):
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
        for transition in list(self.transitions.keys()):
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
        for transition in list(self.transitions.keys()):
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

                if next_combination in list(combinations.values()):
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
        new_fa.K = list(new_fa.states.keys())
        new_fa.is_deterministic = True
        new_fa.sigma = self.sigma
        for eq_class, states in list(new_fa.states.items()):
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
        if self.is_deterministic:
            self.get_states_alphabet()
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
        for state in list(self.states.keys()):
            if self.states[state] == transition:
                return state


    """
        Para auxiliar na criação da gramática regular equivalente,
        são renomeados todos os estados para letras maíusculas do alfabeto
    """
    def get_states_alphabet(self):
        convertion = {}
        self.states = {}
        for i, state in enumerate(self.K):
            convertion[state] = ascii_uppercase[i]
            self.states[ascii_uppercase[i]] = state
        self.K = list(convertion.values())
        self.initial_state = convertion[self.initial_state]
        final_states = self.final_states
        self.final_states = []
        for state in final_states:
            self.final_states.append(convertion[state])
        for transition in self.transitions:
            if len(transition) == 1 and transition.isupper():
                break
            for symbol in self.sigma:
                self.transitions[transition][symbol] = convertion[self.transitions[transition][symbol]]
            self.transitions[convertion[transition]] = self.transitions.pop(transition)

    """
        Retorne se determinada sequencia (input) é aceita pelo automato
    """
    def is_sentence_recognized(self, input):
        automata = self
        if not automata.is_deterministic:
            automata = automata.get_deterministic()

        current_state = automata.initial_state
        for char in input:
            current_state = automata.transitions[current_state][char]
        return current_state in automata.final_states


    """
        Gera sentenças aceitas pelo autômato finito até um tamanho máximo n
    """
    def generate_sentences(self, max_size):
        automata = copy.copy(self)
        if not automata.is_deterministic:
            automata = automata.get_deterministic()
        acceptable = set()
        if automata.initial_state in automata.final_states:
            acceptable.add("&")
        sentence = ""
        acceptable |=(automata.get_acceptable(max_size, automata.initial_state, sentence))
        return list(acceptable)


    """
        Ajuda na recursão da geração das sentenças de tamanho máximo n
    """
    def get_acceptable(self, size_left, current_state, sentence):
        acceptable = set()
        if size_left == 0:
            return acceptable
        for symbol, transition in list(self.transitions[current_state].items()):
            new_sentence = sentence + symbol
            if transition in self.final_states:
                acceptable.add(new_sentence)
            acceptable |= (self.get_acceptable(size_left - 1, transition, new_sentence))
        return acceptable


    """
        Gera sentenças aceitas pelo autômato finito de tamanho EXATAMENTE n
    """
    def get_acceptable_size_n(self, n):
        all_acceptable = self.generate_sentences(n)
        size_n_acceptable = []
        for sentence in all_acceptable:
            if len(sentence) == n:
                size_n_acceptable.append(sentence)
        return size_n_acceptable



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

        #print(pretty)
        return pretty


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
