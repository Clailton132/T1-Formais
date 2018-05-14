class RegGram:
    def  __init__(self):
        self.G = {}
        self.initial_state = None


    def set_initial_state(self, initial_state):
        self.initial_state = initial_state

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
                    self.G[A].append(B)
                    return True
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
