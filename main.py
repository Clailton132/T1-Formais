#!/usr/bin/env python # -*- coding: utf-8 -*
from tkinter import *
import tkinter.messagebox as messagebox
from models import RegGram, Regex
import os, pprint, copy
import pickle

if os.path.isfile("reg_grammar.p"):
    all_reg_grammars = pickle.load( open( "reg_grammar.p", "rb" ) )
    # Var all_reg_grammars returns: {"filename":[g.initial_state, g.G] ... }
    print all_reg_grammars
else:
    all_reg_grammars = {}
    #print "File does not exist"


def get_formatted_production(g):
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

def gui_addRule():
    a = newEntry.get()
    b = newEntry2.get()
    aux = g.add_rule(a,b)
    if aux == True:
        g.add_rule(a,b)
        name = get_formatted_production(g)
        labelText.set(name)
    else:
        name = aux
        labelError.set(name)

    newEntry2.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

def gui_removeRule():
    a = newEntry.get()
    b = newEntry2.get()
    g.remove_rule(a,b)
    name = get_formatted_production(g)
    labelText.set(name)
    newEntry2.delete(0, END)
    return

def gui_checkInput():
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

def gui_saveGrammar():
    filename = filenameEntry.get()
    print "Save Grammar: " + str(filename)
    all_reg_grammars[filename] = [g.initial_state, g.G]
    pickle.dump(all_reg_grammars, open( "reg_grammar.p", "wb" ))

def gui_loadGrammar():
    filename = filenameEntry.get()
    print "Load Grammar: " + str(filename)
    backup = copy.deepcopy(all_reg_grammars[filename])
    g.set_initial_state(backup[0])
    g.G = backup[1]
    pprint.pprint(g.G)
    name = get_formatted_production(g)
    labelText.set(name)



while True:
    os.system('clear')
    print "**********************************"
    print " Trabalho 1: Linguagens Regulares"
    print "**********************************"
    print "* [1] Criar Gramática Regular"
    print "* [2] Listar Gramáticas Salvas"
    print "* [3] Criar Expressão Regular"
    print "* [9] Sair"
    option = raw_input("\nOpção: ")
    if option == "9":
        break
    if option == "2":
        pprint.pprint(all_reg_grammars)
        raw_input("\nAperte para continuar...")
    if option == "1":
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

        buttonAdd = Button(app, text="Add rule", width=20, command=gui_addRule)
        buttonAdd.pack(side='top', padx=15)
        buttonRemove = Button(app, text="Remove rule", width=20, command=gui_removeRule)
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
        button2 = Button(app, text="TEST", width=20, command=gui_checkInput)
        button2.pack(side='top', padx=15,pady=15)


        buttonLoad = Button(app, text="Load Grammar", width=20, command=gui_loadGrammar)
        buttonLoad.pack(side='bottom', padx=15, pady=(0, 30))
        buttonSave = Button(app, text="Save Grammar", width=20, command=gui_saveGrammar)
        buttonSave.pack(side='bottom', padx=15)
        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='bottom')
        Label(app, text="Save / Load Grammar", height=1, font=("Helvetica", 16)).pack(side='bottom')

        app.mainloop()

    # Regex
    if option == "3":
        regex = Regex()
        test = raw_input("Enter regex: ")
        regex.set_regex(test)
        #test = "((ab|ba)?)*"
        print test
        print regex.E
        raw_input("\nAperte para continuar...")
