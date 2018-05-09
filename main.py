from models import RG

g = RG()

#g.add_production('A')
g.add_rule('S', 'aA')
g.add_rule('S', 'bB')
g.add_rule('A', 'a')
g.add_rule('A', 'aB')
g.add_rule('B', 'bB')
g.add_rule('B', 'b')
g.add_rule('B', 'bS')
g.show()
#print "Grammar correct: " + str(g.validate_grammar())
test = "aabbaabbaabbbbb"
print g.check_input_optimized(test)
