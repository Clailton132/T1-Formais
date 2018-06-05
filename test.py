# -*- coding: utf-8 -*-
from models import *
import tkinter as tk
from tkinter import *
import tkinter.messagebox as messagebox
import os, pprint, copy
import pickle

if os.path.isfile("db/reg_gram.p"):
    all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
    # Var all_reg_grammars returns: {"filename":[g.initial_state, g.G] ... }
    #print(all_reg_grammars)
else:
    all_reg_grammars = {}
    #print("File does not exist")

if os.path.isfile("db/regex.p"):
    all_regex = pickle.load( open( "db/regex.p", "rb" ) )
    #print(all_regex)
else:
    all_regex = {}

current_fa = None

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
    print(a)
    print(b)
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
    print("Save Grammar: " + str(filename))
    all_reg_grammars[filename] = [g.initial_state, g.G]
    pickle.dump(all_reg_grammars, open( "db/reg_gram.p", "wb" ))
    messagebox.showinfo("Salvando", "Sua gramática foi salva com sucesso")
    is_saved = True
    filenameEntry.delete(0, END)
    return

"""
    Ação de carregar uma gramática salva anteriormente
"""
def gui_load_grammar():
    filename = filenameEntry.get()
    print("Load Grammar: " + str(filename))
    backup = copy.deepcopy(all_reg_grammars[filename])
    g.set_initial_state(backup[0])
    g.G = backup[1]
    pprint.pprint(g.G)
    name = g.get_pretty()
    labelText.set(name)
    is_saved = True
    return

"""
    Métodos para interface gráfica de expressões regulares
"""

"""
    Ação de setar a expressão regular, ex: "1?(01)*1?"
"""
def gui_set_regex():
    regex = newEntry_regex.get()
    print("regex", regex)
    e.set_regex(regex)
    print("e.E", e.E)
    labelText_regex.set("RE: " + str(regex)+"\n"+str(e.E))
    newEntry_regex.delete(0, END)
    #newEntry.insert(0, 'Default text after button click')
    return

"""
    Salva a expressão regular com filename como parâmetro
"""
def gui_save_regex():
    filename = filenameEntry_regex.get()
    print("Save Regex: " + str(filename))
    all_regex[filename] = [e.literal, e.E]
    pickle.dump(all_regex, open( "db/regex.p", "wb" ))
    messagebox.showinfo("Saving", "Your regex was saved succesfully")
    filenameEntry_regex.delete(0, END)
    return

"""
    Ação de carregar uma expressão regular salva anteriormente
"""
def gui_load_regex():
    filename = filenameEntry_regex.get()
    print("Load Regex: " + str(filename))
    backup = copy.deepcopy(all_regex[filename])
    e.literal = backup[0]
    e.E = backup[1]
    pprint.pprint(e.E)
    name = "RE: " +str(e.literal) + "\n" + str(e.E)
    labelText_regex.set(name)
    return

def gui_gr_af():
    filename = filenameEntry_AF.get()
    backup = copy.deepcopy(all_reg_grammars[filename])
    g.set_initial_state(backup[0])
    g.G = backup[1]
    pprint.pprint(g.G)
    #name = g.get_pretty()
    fa = g.get_eq_automata()
    name = fa.pretty_print()
    labelText_AF.set(name)
    global current_fa
    current_fa = fa


def gui_er_af():
    filename = filenameEntry_AF.get()
    backup = copy.deepcopy(all_regex[filename])
    e.literal = backup[0]
    e.E = backup[1]
    pprint.pprint(e.E)
    name = "RE: " +str(e.literal) + "\n" + str(e.E)
    labelText_regex.set(name)
    fa = e.get_equivalent_automata()
    name = fa.pretty_print()
    labelText_AF.set(name)
    global current_fa
    current_fa = fa

def gui_af_determinize():
    global current_fa
    automata = current_fa.get_deterministic()
    name = automata.pretty_print()
    labelText_AF.set(name)
    current_fa = automata

def gui_af_minimize():
    global current_fa
    automata = current_fa.get_minimized()
    name = automata.pretty_print()
    labelText_AF.set(name)
    current_fa = automata

def gui_af_to_gr():
    rg = current_fa.get_eq_reg_gram()
    name = rg.get_pretty()
    labelText_AF.set(name)




class MainScreen(tk.Tk):

    def __init__(self):

        tk.Tk.__init__(self)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (HomePage, RegGramPage, RegexPage, AF_Page):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(HomePage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Trabalho 1 - Linguagens Formais e Compiladores", font=("Helvetica", 18))
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Linguages Regulares", font=("Helvetica", 26))
        label.pack(pady=10,padx=10)
        label = tk.Label(self, text="Menu", font=("Helvetica", 30))
        label.pack(pady=10,padx=10)

        button = tk.Button(self, text="Gramáticas Regulares", font=("Helvetica", 18),
                            command=lambda: controller.show_frame(RegGramPage))
        button.pack()

        button2 = tk.Button(self, text="Expressões Regulares", font=("Helvetica", 18),
                            command=lambda: controller.show_frame(RegexPage))
        button2.pack()

        button3 = tk.Button(self, text="Autômatos finitos", font=("Helvetica", 18),
                            command=lambda: controller.show_frame(AF_Page))
        button3.pack()


class RegGramPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        #label = tk.Label(self, text="", font=("Helvetica", 16))
        #label.pack(pady=10,padx=10)

        global newEntry
        global newEntry2
        global g
        global labelText
        global labelError
        global newEntry3
        global labelCheckInput
        global filenameEntry
        global is_saved

        button = tk.Button(self,font=("Helvetica", 18), height=1, text="Voltar ao Menu",
                            command=lambda: controller.show_frame(HomePage))
        button.pack()

        g = RegGram()
        is_saved = False

        labelError = tk.StringVar()
        # labelError.set("SOME ERROR")
        label0 = tk.Label(self, textvariable=labelError, height=2)
        label0.pack(padx=3)
        tk.Label(self, text="Gramáticas Regulares", height=1, font=("Helvetica", 28)).pack()
        labelText = tk.StringVar()
        labelText.set("G: P = ")
        label1 = tk.Label(self, textvariable=labelText, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        tk.Label(self, text="Lado esquerdo da produção (ex: S)", height=1, font=("Helvetica", 16)).pack()
        A = tk.StringVar(None)
        newEntry = tk.Entry(self, textvariable=A)
        newEntry.insert(0,"S")
        newEntry.pack()
        tk.Label(self, text="Lado direito da produção (ex: aA)", height=1, font=("Helvetica", 16)).pack()
        B = tk.StringVar(None)
        newEntry2 = tk.Entry(self, textvariable=B)
        newEntry2.insert(0,"")
        newEntry2.pack()

        buttonAdd = tk.Button(self, text="Adicionar regra", width=20, command=gui_add_rule)
        buttonAdd.pack(side='top', padx=15)
        buttonRemove = tk.Button(self, text="Remove regra", width=20, command=gui_remove_rule)
        buttonRemove.pack(side='top', padx=15)

        #tk.Label(self, text="Production Right Side", height=2, font=("Helvetica", 18)).pack()
        labelCheckInput = tk.StringVar()
        label3 = tk.Label(self, textvariable=labelCheckInput, height=1, font=("Helvetica", 14))
        label3.pack()
        tk.Label(self, text="Testar sentença na GR", height=1, font=("Helvetica", 16)).pack()
        input = tk.StringVar(None)
        newEntry3 = tk.Entry(self, textvariable=input)
        newEntry3.insert(0,"")
        newEntry3.pack()
        button2 = tk.Button(self, text="Testar", width=20, command=gui_check_input)
        button2.pack(side='top', padx=15,pady=15)
        tk.Label(self, text="É necessário dar um nome e salvar a gramática.\n Na página de Autômatos finitos você deverá \ninserir este nome", height=2, font=("Helvetica", 14)).pack(side='top')
        button_convert = tk.Button(self, text="Converte para AF", font=('Helvetica', 24), width=20,
                                                    command=lambda: controller.show_frame(AF_Page))
        button_convert.pack(side='top', padx=15,pady=15)


        buttonLoad = tk.Button(self, text="Carregar gramática", width=20, command=gui_load_grammar)
        buttonLoad.pack(side='bottom', padx=15, pady=(0, 30))
        buttonSave = tk.Button(self, text="Salvar gramática", width=20, command=gui_save_grammar)
        buttonSave.pack(side='bottom', padx=15)
        filename = tk.StringVar(None)
        filenameEntry = tk.Entry(self, textvariable=filename)
        filenameEntry.insert(0,"filename")
        filenameEntry.pack(side='bottom')
        tk.Label(self, text="Salvar / Carregar Gramática", height=1, font=("Helvetica", 16)).pack(side='bottom')



class RegexPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        button1 = tk.Button(self, text="Voltar ao Menu", font=("Helvetica", 18),
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        global e
        global newEntry_regex
        global labelText_regex
        global labelError_regex
        global filenameEntry_regex

        e = Regex()


        labelError_regex = tk.StringVar()
        # labelError.set("SOME ERROR")
        label0 = tk.Label(self, textvariable=labelError_regex, height=2)
        label0.pack(padx=3)
        tk.Label(self, text="Expressões Regulares", height=1, font=("Helvetica", 28)).pack()
        labelText_regex = tk.StringVar()
        labelText_regex.set("ER: ")
        label1 = tk.Label(self, textvariable=labelText_regex, height=10, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
        label1.pack()

        tk.Label(self, text="Expressão regular:", height=1, font=("Helvetica", 16)).pack()
        A = tk.StringVar(None)
        newEntry_regex = tk.Entry(self, textvariable=A)
        newEntry_regex.insert(0,"")
        newEntry_regex.pack()

        buttonAdd = tk.Button(self, text="Criar Expressão Regular", width=20, command=gui_set_regex)
        buttonAdd.pack(side='top', padx=15)

        tk.Label(self, text="Salvar / Carregar ER", height=1, font=("Helvetica", 16)).pack(side='top')
        filename = tk.StringVar(None)
        filenameEntry_regex = tk.Entry(self, textvariable=filename)
        filenameEntry_regex.insert(0,"filename")
        filenameEntry_regex.pack(side='top')
        buttonSave = tk.Button(self, text="Salvar ER", width=20, command=gui_save_regex)
        buttonSave.pack(side='top', padx=15)
        buttonLoad = tk.Button(self, text="Carregar ER", width=20, command=gui_load_regex)
        buttonLoad.pack(side='top', padx=15, pady=(0, 30))
        button_convert = tk.Button(self, text="Converte para AF", width=20,
                                                    command=lambda: controller.show_frame(AF_Page))
        button_convert.pack(side='top', padx=15,pady=2)
        tk.Label(self, text="É necessário dar um nome e salvar a gramática.\n Na página de Autômatos finitos você deverá \ninserir este nome", height=3, font=("Helvetica", 14)).pack(side='top')


        # button2 = tk.Button(self, text="Page Two",
        #                     command=lambda: controller.show_frame(PageTwo))
        # button2.pack()

class AF_Page(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        button1 = tk.Button(self, text="Voltar ao Menu", font=("Helvetica", 18),
                            command=lambda: controller.show_frame(HomePage))
        button1.pack()

        global filenameEntry_AF
        global labelText_AF

        tk.Label(self, text="Autômatos Finitos", height=1, font=("Helvetica", 28)).pack()

        tk.Label(self, text="Obter autômato finito equivalente", height=1, font=("Helvetica", 16)).pack(side='top')
        filename = tk.StringVar(None)
        filenameEntry_AF = tk.Entry(self, textvariable=filename)
        filenameEntry_AF.insert(0,"filename")
        filenameEntry_AF.pack(side='top')
        buttonGR = tk.Button(self, text="De uma gramática regular", width=20, command=gui_gr_af)
        buttonGR.pack(side='top', padx=15)
        buttonER = tk.Button(self, text="De uma expressão regular", width=20, command=gui_er_af)
        buttonER.pack(side='top', padx=15, pady=(0, 30))

        labelText_AF = tk.StringVar()
        labelText_AF.set("")
        label1 = tk.Label(self, textvariable=labelText_AF, height=20, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=30,pady=5, anchor="e")
        label1.pack()

        buttonDeterminize = tk.Button(self, text="Determinizar AF", width=20, command=gui_af_determinize)
        buttonDeterminize.pack(side='top', padx=15)

        buttonMinimize = tk.Button(self, text="Minimizar AF", width=20, command=gui_af_minimize)
        buttonMinimize.pack(side='top', padx=15)

        buttonMinimize = tk.Button(self, text="Converter para GR", width=20, command=gui_af_to_gr)
        buttonMinimize.pack(side='top', padx=15)

        tk.Label(self, text="Sentenças", height=1, font=("Helvetica", 16)).pack(side='top')
        sentence = tk.StringVar(None)
        sentenceEntry = tk.Entry(self, textvariable=sentence)
        sentenceEntry.insert(0,"entrada")
        sentenceEntry.pack(side='top')
        buttonTest = tk.Button(self, text="Testar entrada", width=20, command=gui_af_minimize)
        buttonTest.pack(side='top', padx=15, pady=(0, 5))

        size = tk.StringVar(None)
        sizeEntry = tk.Entry(self, textvariable=size)
        sizeEntry.insert(0,"Tamanho")
        sizeEntry.pack(side='top')
        buttonGenerate = tk.Button(self, text="Gerar sentenças de tamanho", width=20, command=gui_af_minimize)
        buttonGenerate.pack(side='top', padx=15, pady=(0, 5))



app = MainScreen()
app.title("Linguagens Regulares")
app.geometry('600x900+200+200')
app.mainloop()
