#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import *
import os, pprint, copy
import pickle

import sys
from PyQt4 import QtGui, QtCore

class ApplicationWidget(QtGui.QWidget):

    def __init__(self):
        super(ApplicationWidget, self).__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(75, 75, 1300, 800)
        self.setWindowTitle('T1 - Linguagens Regulares')

        title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
        item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        """
        --------------------------------------------------------
        --------------------------------------------------------
        * Left Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """

        vbox1 = QtGui.QVBoxLayout()
        vbox1.setSpacing(15)

        vbox1_label = QtGui.QLabel()
        vbox1_label.setText(u'Linguagens Regulares')
        vbox1_label.setFont(title_font)
        vbox1.addWidget(vbox1_label)

        btnCreateGrammar = QtGui.QPushButton(u'Criar Gramática Regular', self)
        btnCreateGrammar.resize(btnCreateGrammar.sizeHint())
        vbox1.addWidget(btnCreateGrammar)

        btnCreateRegex = QtGui.QPushButton(u'Criar Expressão Regular', self)
        btnCreateRegex.resize(btnCreateRegex.sizeHint())
        vbox1.addWidget(btnCreateRegex)

        btnConvertToAutomata = QtGui.QPushButton(u'Conversão para Autômato Finito', self)
        btnConvertToAutomata.resize(btnConvertToAutomata.sizeHint())
        vbox1.addWidget(btnConvertToAutomata)

        btnDeterminize = QtGui.QPushButton(u'Determinizar AF', self)
        btnDeterminize.resize(btnDeterminize.sizeHint())
        vbox1.addWidget(btnDeterminize)

        btnMinimize = QtGui.QPushButton(u'Minimizar AF', self)
        btnMinimize.resize(btnMinimize.sizeHint())
        vbox1.addWidget(btnMinimize)

        btnUnion = QtGui.QPushButton(u'União de 2 AF\'s', self)
        btnUnion.resize(btnUnion.sizeHint())
        vbox1.addWidget(btnUnion)

        btn1 = QtGui.QPushButton(u'...', self)
        btn1.resize(btn1.sizeHint())
        vbox1.addWidget(btn1)

        btn2 = QtGui.QPushButton(u'...', self)
        btn2.resize(btn2.sizeHint())
        vbox1.addWidget(btn2)




        vbox1.addStretch()


        """
        --------------------------------------------------------
        --------------------------------------------------------
                            * Center Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """

        vbox2 = QtGui.QVBoxLayout()
        vbox2.setSpacing(15)

        grammar_label = QtGui.QLabel()
        grammar_label.setText(u'Gramática Regular')
        grammar_label.setFont(subtitle_font)
        vbox2.addWidget(grammar_label)

        """
            Gramática Regular
        """

        gr_name = 'lista2_4a'
        my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        print("Initial State: " + str(my_rg.initial_state))
        print(my_rg.G)
        data = my_rg.G

        table = QtGui.QTableWidget(self)

        n_rows = len(data.keys())
        lengths = [len(x) for x in data.values()]
        n_cols = max(lengths)

        table.setRowCount(n_rows)
        table.setColumnCount(n_cols)

        headers = []
        for n, key in enumerate(sorted(data.keys())):
            headers.append(key)
            for m, item in enumerate(data[key]):
                newitem = QtGui.QTableWidgetItem(item)
                newitem.setFont(item_font)
                table.setItem(n, m, newitem)

        table.setVerticalHeaderLabels(headers)
        for i in range(len(headers)):
            table.verticalHeaderItem(i).setFont(normal_font)
        empty_labels = [" " for x in range(n_cols)]
        table.setHorizontalHeaderLabels(empty_labels)

        table.resizeColumnsToContents()
        table.resizeRowsToContents()

        vbox2.addWidget(table)

        vbox2.addStretch()

        """
        --------------------------------------------------------
        --------------------------------------------------------
                                                   * Right Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """


        vbox3 = QtGui.QVBoxLayout()
        vbox3.setSpacing(15)

        saved_grammar_label = QtGui.QLabel()
        saved_grammar_label.setText(u'Gramáticas Salvas')
        saved_grammar_label.setFont(subtitle_font)
        vbox3.addWidget(saved_grammar_label)


        btn5 = QtGui.QPushButton('GR_1', self)
        btn5.resize(btn5.sizeHint())
        vbox3.addWidget(btn5)

        btn6 = QtGui.QPushButton('GR_2', self)
        btn6.resize(btn6.sizeHint())
        vbox3.addWidget(btn6)

        saved_regex_label = QtGui.QLabel()
        saved_regex_label.setText(u'Expressões Regulares Salvas')
        saved_regex_label.setFont(subtitle_font)
        vbox3.addWidget(saved_regex_label)

        btn7 = QtGui.QPushButton('ER_1', self)
        btn7.resize(btn7.sizeHint())
        vbox3.addWidget(btn7)

        btn8 = QtGui.QPushButton('ER_2', self)
        btn8.resize(btn8.sizeHint())
        vbox3.addWidget(btn8)

        sentence_test_label = QtGui.QLabel()
        sentence_test_label.setText(u'Teste de Sentença')
        sentence_test_label.setFont(subtitle_font)
        vbox3.addWidget(sentence_test_label)

        textbox = QtGui.QLineEdit()
        textbox.setPlaceholderText(u'ex: abba')
        vbox3.addWidget(textbox)

        btn_sentence_test = QtGui.QPushButton('Testar', self)
        btn_sentence_test.resize(btn_sentence_test.sizeHint())
        vbox3.addWidget(btn_sentence_test)


        vbox3.addStretch()

        """
            Add Vertical layouts to grid
        """

        grid.addLayout(vbox1, 0,0)
        grid.addLayout(vbox2, 0,1)
        grid.addLayout(vbox3, 0,2)
        grid.setColumnStretch(0,2)
        grid.setColumnStretch(1,6)
        grid.setColumnStretch(2,2)


        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    w = ApplicationWidget()
    # w.showMaximized()
    app.exec_()


if __name__ == '__main__':
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
    main()
