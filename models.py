class RG:
    def  __init__(self, initial_state='S'):
        self.G = {}
        self.initial_state = initial_state
        self.G[initial_state] = []

    # Productions A -> B
    def add_production(self, A):
        if not self.G.has_key(A):
            if self.validate_production(A):
                self.G[A] = []
                return True
            else:
                print str(A) + " --> is not a valid production, it must be \
                            a Vn (uppercase char) and have length 1. Ex: A"
                return False
        return True

    # Rules B on A -> B
    def add_rule(self, A, B):
        if self.add_production(A):
            if B not in self.G[A]:
                if self.validate_rule(B):
                    self.G[A].append(B)
                else:
                    print "(" +str(B) + ") --> is not a valid production,\nit must be either a Vt (a lower char or digit and have length 1) or a Vt + Vn (a lower char followed by a upper char): Ex: a, aA"

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
                    del self.G[A]

    def validate_grammar(self):
        for prod in self.G:
            if not self.G[prod]:
                return False
        return True

    def is_lower(self, B):
        return B.islower()


    def check_input(self, input):
        return input in self.generate_sequences(len(input))

    def generate_sequences(self, size):
        state = self.initial_state
        final_sequences = []
        sequences = []
        for seq in self.G[state]:
            if self.is_lower(seq):
                final_sequences.append(seq)
            else:
                sequences.append(seq)
        #print "Final Sequences: " + str(final_sequences)
        #print "Sequences: " + str(sequences)
        size -= 1
        while(size > 0):
            size -= 1
            #print "Sequences: " + str(sequences)
            tmp_sequences = sequences[:]
            for seq in tmp_sequences:
                for new_seq in self.G[seq[-1]]:
                    new_seq = seq[0:-1] + new_seq
                    if self.is_lower(new_seq):
                        final_sequences.append(new_seq)
                    else:
                        sequences.append(new_seq)
        return final_sequences

    def check_input_optimized(self, input):
        size = len(input)
        state = self.initial_state
        final_sequences = []
        sequences = []
        for seq in self.G[state]:
            if self.is_lower(seq):
                if (len(seq) == len(input)):
                    final_sequences.append(seq)
            elif (seq[0] == input[0]):
                sequences.append(seq)
        #print "Final Sequences: " + str(final_sequences)
        #print "Sequences[2]: " + str(sequences)
        size -= 1
        i = 1
        while(size > 0):
            size -= 1
            #print "Sequences: " + str(sequences)
            tmp_sequences = sequences[:]
            sequences = []
            for seq in tmp_sequences:
                for new_seq in self.G[seq[-1]]:
                    new_seq = seq[0:-1] + new_seq
                    if self.is_lower(new_seq):
                        if (len(new_seq) == len(input)):
                            final_sequences.append(new_seq)
                    elif (new_seq[i] == input[i]):
                        sequences.append(new_seq)
            i += 1
            #print "Sequences["+str(i+1)+"]: " + str(sequences)
        return (input in final_sequences)





    # Prints the Grammar
    def show(self):
        print self.G
