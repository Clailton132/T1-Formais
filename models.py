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



    # Prints the Grammar
    def show(self):
        print self.G
