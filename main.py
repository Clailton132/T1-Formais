#!/usr/bin/env python # -*- coding: utf-8 -*
from tkinter import *
import tkinter.messagebox as messagebox
from models import *
import os, pprint, copy
import pickle

if os.path.isfile("db/reg_gram.p"):
    all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
    # Var all_reg_grammars returns: {"filename":[g.initial_state, g.G] ... }
    #print all_reg_grammars
else:
    all_reg_grammars = {}
    #print "File does not exist"

if os.path.isfile("db/regex.p"):
    all_regex = pickle.load( open( "db/regex.p", "rb" ) )
    #print all_regex
else:
    all_regex = {}


"""
    Following methods for Tkinter Graphical User Interface
    gui_*
"""

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

while True:
    os.system('clear')
    print "**********************************"
    print " Trabalho 1: Linguagens Regulares"
    print "**********************************"
    print "* [1] Criar Gramática Regular"
    print "* [2] Listar Gramáticas Salvas"
    print "* [3] Criar Expressão Regular"
    print "* [4] Conversão Gramática Regular -> Autômato Finito"
    print "* [5] Conversão Autômato Finito -> Gramática Regular"
    print "* [6] Conversão Expressão Regular -> Autômato Finito"
    print "* [9] Sair"
    option = raw_input("\nOpção: ")
    if option in ("9", ""):
        break
    if option == "2":
        pprint.pprint(all_reg_grammars)
        raw_input("\nAperte para continuar...")
    elif option == "1":
        g = RegGram()
        app = Tk()
        app.title("RegLangs")
        app.geometry('500x800+200+200')

        labelError = StringVar()
        # labelError.set("SOME ERROR")
        label0 = Label(app, textvariable=labelError, height=2)
        label0.pack(padx=3)
        Label(app, text="Regular Grammar Application", height=1, font=("Helvetica", 28)).pack()
        labelText = StringVar()
        labelText.set("G: P = ")
        label1 = Label(app, textvariable=labelText, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        Label(app, text="Production Left Side", height=1, font=("Helvetica", 16)).pack()
        A = StringVar(None)
        newEntry = Entry(app, textvariable=A)
        newEntry.insert(0,"S")
        newEntry.pack()
        Label(app, text="Production Right Side", height=1, font=("Helvetica", 16)).pack()
        B = StringVar(None)
        newEntry2 = Entry(app, textvariable=B)
        newEntry2.insert(0,"")
        newEntry2.pack()

        buttonAdd = Button(app, text="Add rule", width=20, command=gui_add_rule)
        buttonAdd.pack(side='top', padx=15)
        buttonRemove = Button(app, text="Remove rule", width=20, command=gui_remove_rule)
        buttonRemove.pack(side='top', padx=15)

        #Label(app, text="Production Right Side", height=2, font=("Helvetica", 18)).pack()
        labelCheckInput = StringVar()
        label3 = Label(app, textvariable=labelCheckInput, height=1, font=("Helvetica", 14))
        label3.pack()
        Label(app, text="Test Input", height=1, font=("Helvetica", 16)).pack()
        input = StringVar(None)
        newEntry3 = Entry(app, textvariable=input)
        newEntry3.insert(0,"")
        newEntry3.pack()
        button2 = Button(app, text="TEST", width=20, command=gui_check_input)
        button2.pack(side='top', padx=15,pady=15)


        buttonLoad = Button(app, text="Load Grammar", width=20, command=gui_load_grammar)
        buttonLoad.pack(side='bottom', padx=15, pady=(0, 30))
        buttonSave = Button(app, text="Save Grammar", width=20, command=gui_save_grammar)
        buttonSave.pack(side='bottom', padx=15)
        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='bottom')
        Label(app, text="Save / Load Grammar", height=1, font=("Helvetica", 16)).pack(side='bottom')

        app.mainloop()

    # Regex
    elif option == "3":
        e = Regex()
        app = Tk()
        app.title("RegLangs")
        app.geometry('500x800+200+200')

        Label(app, text="Save / Load Regex", height=1, font=("Helvetica", 16)).pack(side='top')
        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='top')
        buttonSave = Button(app, text="Save Regex", width=20, command=gui_save_regex)
        buttonSave.pack(side='top', padx=15)
        buttonLoad = Button(app, text="Load Regex", width=20, command=gui_load_regex)
        buttonLoad.pack(side='top', padx=15, pady=(0, 30))


        labelError = StringVar()
        # labelError.set("SOME ERROR")
        label0 = Label(app, textvariable=labelError, height=2)
        label0.pack(padx=3)
        Label(app, text="Regular Expression Application", height=1, font=("Helvetica", 28)).pack()
        labelText = StringVar()
        labelText.set("RE: ")
        label1 = Label(app, textvariable=labelText, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        Label(app, text="Regular expression:", height=1, font=("Helvetica", 16)).pack()
        A = StringVar(None)
        newEntry = Entry(app, textvariable=A)
        newEntry.insert(0,"")
        newEntry.pack()

        buttonAdd = Button(app, text="Set regex", width=20, command=gui_set_regex)
        buttonAdd.pack(side='top', padx=15)


        app.mainloop()


    elif option == "4":
        pprint.pprint(all_reg_grammars)
        gr_name = raw_input("Name of the Regular Grammar filename: ")
        my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        print "Initial State: " + str(my_rg.initial_state)
        print my_rg.G
        fa = my_rg.get_eq_automata()
        pretty = fa.pretty_print()

    elif option == "5":
        # test = 'gramatica_a_par'
        #test = 'gr_main'
        test = 'gr_11a'
        rg = RegGram(all_reg_grammars[test][1],all_reg_grammars[test][0])
        rg.show()
        fa = rg.get_eq_automata()
        fa.pretty_print()

        print "Deterministic: "
        dfa = fa.get_deterministic()
        dfa.pretty_print()

        # TODO: fix get_eq_reg_gram() to deterministic fa version
        # new_rg = fa.get_eq_reg_gram()
        # new_rg.show()
        pause = raw_input("...")

    elif option == "6":
        # teste
        r = Regex()
        test = raw_input("Regular expression: ")
        r.set_regex(test)
        print r.E
        tree = r.get_equivalent_automata()
        r.print_tree(tree)
        print "Threaded"
        r.fill_threaded_tree(tree)
        r.print_threaded_tree(tree)
        r.fill_states_composing(tree)
        print r.print_composing(tree)
        pause = raw_input("...")
