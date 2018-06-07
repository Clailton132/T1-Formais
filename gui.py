#!/usr/bin/env python
# -*- coding: utf-8 -*-
from models import *
import os, pprint, copy
import pickle

import sys
from PyQt4 import QtGui, QtCore

class CreateGrammarWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CreateGrammarWidget, self).__init__()
        self.initUI()
        self.g = RegGram()


    def initUI(self):
        self.setGeometry(75, 75, 800, 800)
        self.setWindowTitle(u'Gramáticas Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        vbox1 = QtGui.QVBoxLayout()
        vbox1.setSpacing(15)
        vbox2 = QtGui.QVBoxLayout()
        vbox2.setSpacing(15)

        vbox1_label = QtGui.QLabel()
        vbox1_label.setText(u'Gramáticas Regulares')
        vbox1_label.setFont(self.title_font)
        vbox1.addWidget(vbox1_label)

        # gr_name = 'lista2_4a'
        # my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        # print("Initial State: " + str(my_rg.initial_state))
        # print(my_rg.G)

        self.table = QtGui.QTableWidget(self)
        vbox1.addWidget(self.table)

        vbox1_label = QtGui.QLabel()
        vbox1_label.setText(u'Ações')
        vbox1_label.setFont(self.subtitle_2_font)
        vbox1.addWidget(vbox1_label)

        production_grid = QtGui.QGridLayout()

        self.A_textbox = QtGui.QLineEdit()
        self.A_textbox.setPlaceholderText(u'ex: \"S\"')
        production_grid.addWidget(self.A_textbox, 0,0)

        arrow_label = QtGui.QLabel()
        arrow_label.setText(u'----->')
        arrow_label.setFont(self.title_font)
        production_grid.addWidget(arrow_label, 0,1)

        self.B_textbox = QtGui.QLineEdit()
        self.B_textbox.setPlaceholderText(u'ex: \"aS\"')
        production_grid.addWidget(self.B_textbox, 0,2)

        vbox1.addLayout(production_grid)

        btnAddRule = QtGui.QPushButton(u'Adicionar regra à produção', self)
        btnAddRule.resize(btnAddRule.sizeHint())
        btnAddRule.clicked.connect(self.signal_add_rule)
        vbox1.addWidget(btnAddRule)

        btnRemoveRule = QtGui.QPushButton(u'Remover regra da produção', self)
        btnRemoveRule.resize(btnRemoveRule.sizeHint())
        btnRemoveRule.clicked.connect(self.signal_remove_rule)
        vbox1.addWidget(btnRemoveRule)

        vbox1.addStretch()

        vbox2_label = QtGui.QLabel()
        vbox2_label.setText(u'Salvar Gramática')
        vbox2_label.setFont(self.subtitle_font)
        vbox2.addWidget(vbox2_label)

        filename_label = QtGui.QLabel()
        filename_label.setText(u'Nome do arquivo')
        filename_label.setFont(self.subtitle_2_font)
        vbox2.addWidget(filename_label)

        self.save_textbox = QtGui.QLineEdit()
        self.save_textbox.setPlaceholderText(u'ex: \"gramatica_1\"')
        vbox2.addWidget(self.save_textbox)

        btn_save_grammar = QtGui.QPushButton(u'Salvar', self)
        btn_save_grammar.resize(btn_save_grammar.sizeHint())
        btn_save_grammar.clicked.connect(self.signal_save_grammar)
        vbox2.addWidget(btn_save_grammar)

        load_grammar_label = QtGui.QLabel()
        load_grammar_label.setText(u'Carregar nova Gramática')
        load_grammar_label.setFont(self.subtitle_2_font)
        vbox2.addWidget(load_grammar_label)

        self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox2.addWidget(self.grammar_list)

        btn_load_grammar = QtGui.QPushButton(u'Carregar', self)
        btn_load_grammar.resize(btn_load_grammar.sizeHint())
        btn_load_grammar.clicked.connect(self.signal_load_grammar)
        vbox2.addWidget(btn_load_grammar)


        vbox2.addStretch()

        grid.setColumnStretch(0,3)
        grid.setColumnStretch(1,2)
        grid.addLayout(vbox1, 0,0)
        grid.addLayout(vbox2, 0,1)


    def refresh_grammar(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        data = self.g.G
        initial_state = self.g.initial_state
        print data
        if data:
            n_rows = len(data.keys())
            lengths = [len(x) for x in data.values()]
            n_cols = max(lengths)

            self.table.setRowCount(n_rows)
            self.table.setColumnCount(n_cols)


            headers = []
            ordered_data = sorted(data.keys())
            ordered_data.remove(initial_state)
            ordered_data = [initial_state] + ordered_data
            for n, key in enumerate(ordered_data):
                headers.append(key)
                for m, item in enumerate(data[key]):
                    newitem = QtGui.QTableWidgetItem(item)
                    # newitem.setFont(self.item_font)
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(n, m, newitem)

            self.table.setVerticalHeaderLabels(headers)
            for i in range(len(headers)):
                self.table.verticalHeaderItem(i).setFont(self.subtitle_2_font)
            empty_labels = [" " for x in range(n_cols)]
            self.table.setHorizontalHeaderLabels(empty_labels)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    def refresh_grammar_list(self):
        all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
        print all_reg_grammars.keys()
        self.grammar_list.clear()
        # self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)

    """
        Ação de adicionar regra numa gramática regular
    """
    def signal_add_rule(self):
        a = str(self.A_textbox.text())
        b = str(self.B_textbox.text())
        aux = self.g.add_rule(a,b)
        if aux == True:
            self.g.add_rule(a,b)
            self.refresh_grammar()
        else:
            if aux:
                name = aux.decode("utf-8")
                QtGui.QMessageBox.information(self, "Erro", name)
        # newEntry2.delete(0, END)
        return


    """
        Ação de remover regra numa gramática regular
    """
    def signal_remove_rule(self):
        a = str(self.A_textbox.text())
        b = str(self.B_textbox.text())
        self.g.remove_rule(a,b)
        self.refresh_grammar()
        # else:
            # name = aux.decode("utf-8")
            # QtGui.QMessageBox.information(self, "Erro", name)
        # newEntry2.delete(0, END)
        return

    """
        Ação de testar sentenças de uma gramática
    """
    def signal_check_input(self):

        return

    """
        Ação de salvar a gramática em arquivo "filename"
    """
    def signal_save_grammar(self):
        filename = str(self.save_textbox.text())
        print("Save Grammar: " + str(filename))
        all_reg_grammars[filename] = [self.g.initial_state, self.g.G]
        pickle.dump(all_reg_grammars, open( "db/reg_gram.p", "wb" ))
        self.refresh_grammar_list()
        QtGui.QMessageBox.information(self, u'Salvando', u'Sua gramática foi salva com sucesso')
        # filenameEntry.delete(0, END)
        return

    """
        Ação de carregar uma gramática salva anteriormente
    """
    def signal_load_grammar(self):
        filename = str(self.grammar_list.currentItem().text())
        all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
        [self.g.initial_state, self.g.G] = all_reg_grammars[filename]
        self.refresh_grammar()

        return

    def list_grammar_clicked(self,item):
        pass
        # QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

class ApplicationWidget(QtGui.QWidget):

    def __init__(self):
        super(ApplicationWidget, self).__init__()
        self.initUI()
        self.g = RegGram


    def initUI(self):
        self.setGeometry(75, 75, 1200, 800)
        self.setWindowTitle('T1 - Linguagens Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 16, QtGui.QFont.Bold)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

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
        vbox1_label.setFont(self.title_font)
        vbox1.addWidget(vbox1_label)

        self.grammar_dialog = CreateGrammarWidget(self)

        btnCreateGrammar = QtGui.QPushButton(u'Criar/Editar Gramática Regular', self)
        btnCreateGrammar.resize(btnCreateGrammar.sizeHint())
        btnCreateGrammar.clicked.connect(self.create_grammar_signal)
        vbox1.addWidget(btnCreateGrammar)

        btnCreateRegex = QtGui.QPushButton(u'Criar/Editar Expressão Regular', self)
        btnCreateRegex.resize(btnCreateRegex.sizeHint())
        vbox1.addWidget(btnCreateRegex)

        current_actions_label = QtGui.QLabel()
        current_actions_label.setText(u'Ações com o modelo atual')
        current_actions_label.setFont(self.subtitle_font)
        vbox1.addWidget(current_actions_label)

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
        grammar_label.setFont(self.subtitle_font)
        vbox2.addWidget(grammar_label)

        """
            Gramática Regular
        """

        self.table = QtGui.QTableWidget(self)
        vbox2.addWidget(self.table)

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
        saved_grammar_label.setFont(self.subtitle_font)
        vbox3.addWidget(saved_grammar_label)

        self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox3.addWidget(self.grammar_list)

        btnRefreshGrammarList = QtGui.QPushButton(u'Atualizar lista', self)
        btnRefreshGrammarList.resize(btnRefreshGrammarList.sizeHint())
        btnRefreshGrammarList.clicked.connect(self.refresh_grammar_list)
        vbox3.addWidget(btnRefreshGrammarList)

        btnGetGrammar = QtGui.QPushButton(u'Carregar Gramática', self)
        btnGetGrammar.resize(btnGetGrammar.sizeHint())
        btnGetGrammar.clicked.connect(self.get_grammar_from_list)
        vbox3.addWidget(btnGetGrammar)



        saved_regex_label = QtGui.QLabel()
        saved_regex_label.setText(u'Expressões Regulares Salvas')
        saved_regex_label.setFont(self.subtitle_font)
        vbox3.addWidget(saved_regex_label)

        regex_list = QtGui.QListWidget()
        list_all_regex = all_regex.keys()
        regex_list.addItems(list_all_regex)

        vbox3.addWidget(regex_list)

        btnGetRegex = QtGui.QPushButton(u'Carregar Expressão Regular', self)
        btnGetRegex.resize(btnGetRegex.sizeHint())
        vbox3.addWidget(btnGetRegex)


        sentence_test_label = QtGui.QLabel()
        sentence_test_label.setText(u'Teste de Sentença')
        sentence_test_label.setFont(self.subtitle_font)
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
        grid.setColumnStretch(0,2)
        grid.addLayout(vbox2, 0,1)
        grid.setColumnStretch(1,6)
        grid.addLayout(vbox3, 0,2)
        grid.setColumnStretch(2,2)


        self.show()


    def list_grammar_clicked(self,item):
        pass
      # QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

    def create_grammar_signal(self):
        self.grammar_dialog.show()

    def refresh_grammar_list(self):
        all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
        print all_reg_grammars.keys()
        self.grammar_list.clear()
        # self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)

    def refresh_grammar(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        data = self.g.G
        initial_state = self.g.initial_state
        print data
        if data:
            n_rows = len(data.keys())
            lengths = [len(x) for x in data.values()]
            n_cols = max(lengths)

            self.table.setRowCount(n_rows)
            self.table.setColumnCount(n_cols)


            headers = []
            ordered_data = sorted(data.keys())
            ordered_data.remove(initial_state)
            ordered_data = [initial_state] + ordered_data
            for n, key in enumerate(ordered_data):
                headers.append(key)
                for m, item in enumerate(data[key]):
                    newitem = QtGui.QTableWidgetItem(item)
                    # newitem.setFont(self.item_font)
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(n, m, newitem)

            self.table.setVerticalHeaderLabels(headers)
            for i in range(len(headers)):
                self.table.verticalHeaderItem(i).setFont(self.subtitle_2_font)
            empty_labels = [" " for x in range(n_cols)]
            self.table.setHorizontalHeaderLabels(empty_labels)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    def get_grammar_from_list(self):
        filename = str(self.grammar_list.currentItem().text())
        all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
        [self.g.initial_state, self.g.G] = all_reg_grammars[filename]
        self.refresh_grammar()




def main():
    app = QtGui.QApplication(sys.argv)
    w = ApplicationWidget()
    w.showMaximized()
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
