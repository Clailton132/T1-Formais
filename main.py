from models import RG
from tkinter import *
import pprint
import tkinter.messagebox

g = RG()

def gui_addRule():
    a = newEntry.get()
    b = newEntry2.get()
    g.add_rule(a,b)
    lines = "G: P = {\n"
    for production in g.G.keys():
        rules = ""
        for rule in g.G[production]:
            rules += str(rule) + " | "
        rules = rules[0:-3]
        lines += (str(production) + "-> " + rules + "\n")
    lines += "}"
    name = lines
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


app = Tk()
app.title("RegLangs")
app.geometry('1200x700+200+200')

labelError = StringVar()
# labelError.set("SOME ERROR")
label0 = Label(app, textvariable=labelError, height=1)
label0.pack()
Label(app, text="Regular Grammar Application", height=2, font=("Helvetica", 32)).pack()
labelText = StringVar()
labelText.set("G: P = ")
label1 = Label(app, textvariable=labelText, height=6, font=("Helvetica", 16), borderwidth=2, relief="groove", padx=60,pady=15)
label1.pack()

Label(app, text="Production Left Side", height=2, font=("Helvetica", 16)).pack()
A = StringVar(None)
newEntry = Entry(app, textvariable=A)
newEntry.insert(0,"S")
newEntry.pack()
Label(app, text="Production Right Side", height=2, font=("Helvetica", 16)).pack()
B = StringVar(None)
newEntry2 = Entry(app, textvariable=B)
newEntry2.insert(0,"")
newEntry2.pack()

button1 = Button(app, text="Add rule", width=20, command=gui_addRule)
button1.pack(side='top', padx=15,pady=15)


Label(app, text="Test input", height=2, font=("Helvetica", 24)).pack()
#Label(app, text="Production Right Side", height=2, font=("Helvetica", 18)).pack()
labelCheckInput = StringVar()
label3 = Label(app, textvariable=labelCheckInput, height=2, font=("Helvetica", 14))
label3.pack()
Label(app, text="Input", height=2, font=("Helvetica", 12)).pack()
input = StringVar(None)
newEntry3 = Entry(app, textvariable=input)
newEntry3.insert(0,"")
newEntry3.pack()
button2 = Button(app, text="TEST", width=20, command=gui_checkInput)
button2.pack(side='top', padx=15,pady=15)


app.mainloop()
