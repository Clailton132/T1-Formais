from string import ascii_uppercase

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
        descript.append("       |")
        hr = "-----------"
        symbols = []
        for symbol in self.sigma:
            if symbol not in symbols:
                symbols.append(symbol)
                if self.deterministic:
                    descript[0] += ""+ str(symbol) + self.print_spaces(1) + "|"
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
                descript[1] += "" + str(self.get_name_of_state(self.transitions[self.initial_state][symbol])) + self.print_spaces(1)+ "|"
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
                            descript[i] += "" + str(self.get_name_of_state(self.transitions[state][symbol])) + self.print_spaces(1) + "|"
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
        x = raw_input("\n\n...")
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
