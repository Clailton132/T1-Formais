from string import ascii_uppercase

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
        #print "Final sentences: " + str(final_sentences)
        #print "sentences: " + str(sentences)
        size -= 1
        while(size > 0):
            size -= 1
            #print "sentences: " + str(sentences)
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
        #print "Final sentences: " + str(final_sentences)
        #print "sentences[2]: " + str(sentences)
        size -= 1
        i = 1
        while(size > 0):
            size -= 1
            #print "sentences: " + str(sentences)
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
            #print "sentences["+str(i+1)+"]: " + str(sentences)
        return (input in final_sentences)

    # Prints the Grammar
    def show(self):
        print self.G

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
            fa.transitions[new_symbol][rule] = [new_symbol]


        fa.pretty_print()
        return fa


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



class FiniteAutomata:
    def  __init__(self, K=[], sigma=[], transitions={}, initial_state=None, final_states=[]):
        self.K = K
        self.sigma = sigma
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states


    """
        Prints the finite automata as a table to improve interpretability
    """
    def pretty_print(self):
        bigger = self.get_max_column_size() * 5
        descript = []
        descript.append("       |")
        hr = "-----------"
        symbols = []
        for symbol in self.sigma:
            if symbol not in symbols:
                symbols.append(symbol)
                descript[0] += "   "+ str(symbol) + self.print_spaces(bigger-((1)*5)) + " |"
                hr += "----------"

        str_final = " "
        if self.initial_state in self.final_states:
            str_final = "*"
        descript.append(str_final + "->" + str(self.initial_state) + "   |")
        for symbol in symbols:
            size = len(self.transitions[self.initial_state][symbol])
            descript[1] += "" + str(self.transitions[self.initial_state][symbol]) + self.print_spaces(bigger-((size)*5))+ "|"

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
                        descript[i] += "" + str(self.transitions[state][symbol]) + self.print_spaces(bigger-((size)*5)) + "|"
                    else:
                        descript[i] += "" + "----" + " |"
                i += 1


        pretty = descript[0]+"\n"+hr+"\n"
        for line in descript[1:]:
            pretty += line + "\n"

        print pretty
        x = raw_input("\n\n...")
        return pretty


    """
        Returns the size of the max column to improve pretty print
    """
    def get_max_column_size(self):
        max = 0
        for symbol in self.K:
            for rule in self.transitions[symbol]:
                size = len(self.transitions[symbol][rule])
                if size > max:
                    max = size
        return max

    """
        Prints 'n' blank spaces
    """
    def print_spaces(self,n):
        s = ""
        for _ in range(n):
            s += " "
        return s
