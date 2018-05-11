#!/usr/bin/env python # -*- coding: utf-8 -*
from tkinter import *
import tkinter.messagebox
from models import RG
import os, pprint, copy
import pickle

if os.path.isfile("reg_grammar.p"):
    all_reg_grammars = pickle.load( open( "reg_grammar.p", "rb" ) )
    print all_reg_grammars
else:
    all_reg_grammars = {}
    #print "File does not exist"


def get_formatted_production(g):
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
    g.add_rule(a,b)
    name = get_formatted_production(g)
    labelText.set(name)
    #newEntry.delete(0, END)
    newEntry2.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

def gui_checkInput():
    input = newEntry3.get()
    text = "Your grammar G is not correct!"
    if(g.validate_grammar()):
        text = "Sorry! Your input is not accepted by the grammar G"
        if g.check_input_optimized(input):
            text = "Your input is accepted by the grammar G"
    labelCheckInput.set(text)

def gui_saveGrammar():
    filename = filenameEntry.get()
    print "Save Grammar: " + str(filename)
    all_reg_grammars[filename] = g.G
    pickle.dump(all_reg_grammars, open( "reg_grammar.p", "wb" ))

def gui_loadGrammar():
    filename = filenameEntry.get()
    print "Load Grammar: " + str(filename)
    g.G = copy.deepcopy(all_reg_grammars[filename])
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
        g = RG()
        app = Tk()
        app.title("RegLangs")
        app.geometry('500x800+200+200')

        labelError = StringVar()
        # labelError.set("SOME ERROR")
        label0 = Label(app, textvariable=labelError, height=1)
        label0.pack()
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

        button1 = Button(app, text="Add rule", width=20, command=gui_addRule)
        button1.pack(side='top', padx=15,pady=15)

        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack()
        buttonLoad = Button(app, text="Load Grammar", width=20, command=gui_loadGrammar)
        buttonLoad.pack(side='top', padx=15,pady=5)
        buttonSave = Button(app, text="Save Grammar", width=20, command=gui_saveGrammar)
        buttonSave.pack(side='top', padx=15,pady=5)


        Label(app, text="Test input", height=1, font=("Helvetica", 24)).pack()
        #Label(app, text="Production Right Side", height=2, font=("Helvetica", 18)).pack()
        labelCheckInput = StringVar()
        label3 = Label(app, textvariable=labelCheckInput, height=1, font=("Helvetica", 14))
        label3.pack()
        Label(app, text="Input", height=1, font=("Helvetica", 12)).pack()
        input = StringVar(None)
        newEntry3 = Entry(app, textvariable=input)
        newEntry3.insert(0,"")
        newEntry3.pack()
        button2 = Button(app, text="TEST", width=20, command=gui_checkInput)
        button2.pack(side='top', padx=15,pady=15)
        app.mainloop()
