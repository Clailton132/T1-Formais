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
    Os seguintes métodos são utilizados para interface gráfica da biblioteca Tkinter
    gui_*
"""

"""
    Ação de adicionar regra numa gramática regular
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
        messagebox.showinfo("Erro", name)

    newEntry2.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return


"""
    Ação de remover regra numa gramática regular
"""
def gui_remove_rule():
    a = newEntry.get()
    b = newEntry2.get()
    g.remove_rule(a,b)
    name = g.get_pretty()
    labelText.set(name)
    newEntry2.delete(0, END)
    return

"""
    Ação de testar sentenças de uma gramática
"""
def gui_check_input():
    input = newEntry3.get()
    text = "Sua gramática G não está correta!"
    if(g.validate_grammar()):
        text = "Sua entrada NÃO é aceita pela gramática G"
        if g.check_input_optimized(input):
            text = "Sua entrada é aceita pela gramática G"
            messagebox.showinfo("Teste de sentença", text)
        else:
            messagebox.showerror("Teste de sentença", text)

    labelCheckInput.set(text)
    return

"""
    Ação de salvar a gramática em arquivo "filename"
"""
def gui_save_grammar():
    filename = filenameEntry.get()
    print "Save Grammar: " + str(filename)
    all_reg_grammars[filename] = [g.initial_state, g.G]
    pickle.dump(all_reg_grammars, open( "db/reg_gram.p", "wb" ))
    messagebox.showinfo("Salvando", "Sua gramática foi salva com sucesso")
    filenameEntry.delete(0, END)
    return

"""
    Ação de carregar uma gramática salva anteriormente
"""
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

"""
    Métodos para interface gráfica de expressões regulares
"""

"""
    Ação de setar a expressão regular, ex: "1?(01)*1?"
"""
def gui_set_regex():
    regex = newEntry.get()
    e.set_regex(regex)
    labelText.set("RE: " + str(regex)+"\n"+str(e.E))
    newEntry.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

"""
    Salva a expressão regular com filename como parâmetro
"""
def gui_save_regex():
    filename = filenameEntry.get()
    print "Save Regex: " + str(filename)
    all_regex[filename] = [e.literal, e.E]
    pickle.dump(all_regex, open( "db/regex.p", "wb" ))
    messagebox.showinfo("Saving", "Your regex was saved succesfully")
    filenameEntry.delete(0, END)
    return

"""
    Ação de carregar uma expressão regular salva anteriormente
"""
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
        app.title("Linguagens Regulares")
        app.geometry('500x800+200+200')

        labelError = StringVar()
        # labelError.set("SOME ERROR")
        label0 = Label(app, textvariable=labelError, height=2)
        label0.pack(padx=3)
        Label(app, text="Gramáticas Regulares", height=1, font=("Helvetica", 28)).pack()
        labelText = StringVar()
        labelText.set("G: P = ")
        label1 = Label(app, textvariable=labelText, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        Label(app, text="Lado esquerdo da produção (ex: S)", height=1, font=("Helvetica", 16)).pack()
        A = StringVar(None)
        newEntry = Entry(app, textvariable=A)
        newEntry.insert(0,"S")
        newEntry.pack()
        Label(app, text="Lado direito da produção (ex: aA)", height=1, font=("Helvetica", 16)).pack()
        B = StringVar(None)
        newEntry2 = Entry(app, textvariable=B)
        newEntry2.insert(0,"")
        newEntry2.pack()

        buttonAdd = Button(app, text="Adicionar regra", width=20, command=gui_add_rule)
        buttonAdd.pack(side='top', padx=15)
        buttonRemove = Button(app, text="Remove regra", width=20, command=gui_remove_rule)
        buttonRemove.pack(side='top', padx=15)

        #Label(app, text="Production Right Side", height=2, font=("Helvetica", 18)).pack()
        labelCheckInput = StringVar()
        label3 = Label(app, textvariable=labelCheckInput, height=1, font=("Helvetica", 14))
        label3.pack()
        Label(app, text="Testar sentença na GR", height=1, font=("Helvetica", 16)).pack()
        input = StringVar(None)
        newEntry3 = Entry(app, textvariable=input)
        newEntry3.insert(0,"")
        newEntry3.pack()
        button2 = Button(app, text="Testar", width=20, command=gui_check_input)
        button2.pack(side='top', padx=15,pady=15)


        buttonLoad = Button(app, text="Carregar gramática", width=20, command=gui_load_grammar)
        buttonLoad.pack(side='bottom', padx=15, pady=(0, 30))
        buttonSave = Button(app, text="Salvar gramática", width=20, command=gui_save_grammar)
        buttonSave.pack(side='bottom', padx=15)
        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='bottom')
        Label(app, text="Salvar / Carregar Gramática", height=1, font=("Helvetica", 16)).pack(side='bottom')

        app.mainloop()

    # Regex
    elif option == "3":
        e = Regex()
        app = Tk()
        app.title("Linguagens Regulares")
        app.geometry('500x800+200+200')

        Label(app, text="Salvar / Carregar ER", height=1, font=("Helvetica", 16)).pack(side='top')
        filename = StringVar(None)
        filenameEntry = Entry(app, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='top')
        buttonSave = Button(app, text="Salvar ER", width=20, command=gui_save_regex)
        buttonSave.pack(side='top', padx=15)
        buttonLoad = Button(app, text="Carregar ER", width=20, command=gui_load_regex)
        buttonLoad.pack(side='top', padx=15, pady=(0, 30))


        labelError = StringVar()
        # labelError.set("SOME ERROR")
        label0 = Label(app, textvariable=labelError, height=2)
        label0.pack(padx=3)
        Label(app, text="Expressões Regulares", height=1, font=("Helvetica", 28)).pack()
        labelText = StringVar()
        labelText.set("ER: ")
        label1 = Label(app, textvariable=labelText, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        Label(app, text="Expressão regular:", height=1, font=("Helvetica", 16)).pack()
        A = StringVar(None)
        newEntry = Entry(app, textvariable=A)
        newEntry.insert(0,"")
        newEntry.pack()

        buttonAdd = Button(app, text="Criar Expressão Regular", width=20, command=gui_set_regex)
        buttonAdd.pack(side='top', padx=15)

        app.mainloop()


    elif option == "4":
        # pprint.pprint(all_reg_grammars)
        # gr_name = raw_input("Name of the Regular Grammar filename: ")
        gr_name = 'example_1'
        my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        print "Initial State: " + str(my_rg.initial_state)
        print my_rg.G
        fa = my_rg.get_eq_automata()
        pretty = fa.pretty_print()

        pause = raw_input("...")

    elif option == "5":
        # test = 'gramatica_a_par'
        #test = 'gr_main'
        test = 'example_1'
        rg = RegGram(all_reg_grammars[test][1],all_reg_grammars[test][0])
        rg.show()
        fa = rg.get_eq_automata()
        fa.pretty_print()

        print "Deterministic: "
        dfa = fa.get_deterministic()
        dfa.pretty_print()

        print "Minimized: "
        minimized_dfa = dfa.get_minimized()
        minimized_dfa.pretty_print()

        # print "Equivalent Grammar"
        # # TODO: fix get_eq_reg_gram() to deterministic fa version
        # new_rg = minimized_dfa.get_eq_reg_gram()
        # new_rg.show()
        pause = raw_input("...")

    elif option == "6":
        # teste
        r = Regex()
        test = raw_input("Regular expression: ")
        r.set_regex(test)
        print r.E
        automata = r.get_equivalent_automata()
        automata.pretty_print()
        pause = raw_input("...")
