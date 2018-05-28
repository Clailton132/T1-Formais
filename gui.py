def gui_add_rule():
    a = newEntry.get()
    b = newEntry2.get()
    aux = g.add_rule(a,b)
    if aux == True:
        g.add_rule(a,b)
        name = g.get_pretty()
        labelText.set(name)
    else:
        name = aux
        labelError.set(name)
        messagebox.showinfo("Error", name)

    newEntry2.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

def gui_remove_rule():
    a = newEntry.get()
    b = newEntry2.get()
    g.remove_rule(a,b)
    name = g.get_pretty()
    labelText.set(name)
    newEntry2.delete(0, END)
    return

def gui_check_input():
    input = newEntry3.get()
    text = "Your grammar G is not correct!"
    if(g.validate_grammar()):
        text = "Your input is NOT accepted by the grammar G"
        if g.check_input_optimized(input):
            text = "Your input is accepted by the grammar G"
            messagebox.showinfo("Testing input", text)
        else:
            messagebox.showerror("Testing input", text)

    labelCheckInput.set(text)
    return

def gui_save_grammar():
    filename = filenameEntry.get()
    print "Save Grammar: " + str(filename)
    all_reg_grammars[filename] = [g.initial_state, g.G]
    pickle.dump(all_reg_grammars, open( "db/reg_gram.p", "wb" ))
    return

def gui_load_grammar():
    filename = filenameEntry.get()
    print "Load Grammar: " + str(filename)
    backup = copy.deepcopy(all_reg_grammars[filename])
    g.set_initial_state(backup[0])
    g.G = backup[1]
    pprint.pprint(g.G)
    name = g.get_pretty()
    labelText.set(name)
    return

def gui_set_regex():
    regex = newEntry.get()
    e.set_regex(regex)
    labelText.set("RE: " + str(regex)+"\n"+str(e.E))
    newEntry.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

def gui_save_regex():
    filename = filenameEntry.get()
    print "Save Regex: " + str(filename)
    all_regex[filename] = [e.literal, e.E]
    pickle.dump(all_regex, open( "db/regex.p", "wb" ))
    return

def gui_load_regex():
    filename = filenameEntry.get()
    print "Load Regex: " + str(filename)
    backup = copy.deepcopy(all_regex[filename])
    e.literal = backup[0]
    e.E = backup[1]
    pprint.pprint(e.E)
    name = "RE: " +str(e.literal) + "\n" + str(e.E)
    labelText.set(name)
    return
