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
                    if fa.transitions[symbol][rule[0]] and fa.transitions[symbol][rule[0]] != ["-"]:
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

class Regex:
    def  __init__(self):
        self.literal = ""
        self.E = []

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
        self.E = context[0][0]

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
