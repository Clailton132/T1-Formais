#!/usr/bin/env python

from models import *
import os, pprint, copy
import pickle

import sys
from PyQt5 import QtGui, QtWidgets, QtCore

class ApplicationWidget(QtWidgets.QWidget):

    def __init__(self):
        super(ApplicationWidget, self).__init__()
        self.initUI()
        self.g = RegGram()
        self.e = Regex()
        self.is_current_a_grammar = False
        self.automatas = list()


    def initUI(self):
        self.setGeometry(75, 75, 1300, 800)
        self.setWindowTitle('T1 - Linguagens Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        self.normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        """
        --------------------------------------------------------
        --------------------------------------------------------
        * Left Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """

        vbox_left = QtWidgets.QVBoxLayout()
        vbox_left.setSpacing(15)

        vbox_left_label = QtWidgets.QLabel()
        vbox_left_label.setText('Linguagens Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)

        self.grammar_dialog = CreateGrammarWidget(self)

        btnCreateGrammar = QtWidgets.QPushButton('Criar/Editar Gramática Regular', self)
        btnCreateGrammar.resize(btnCreateGrammar.sizeHint())
        btnCreateGrammar.clicked.connect(self.create_grammar_signal)
        vbox_left.addWidget(btnCreateGrammar)

        self.regex_dialog = CreateRegexWidget(self)

        btnCreateRegex = QtWidgets.QPushButton('Criar/Editar Expressão Regular', self)
        btnCreateRegex.resize(btnCreateRegex.sizeHint())
        btnCreateRegex.clicked.connect(self.create_regex_signal)
        vbox_left.addWidget(btnCreateRegex)

        current_actions_label = QtWidgets.QLabel()
        current_actions_label.setText('Ações com o modelo atual')
        current_actions_label.setFont(self.subtitle_font)
        vbox_left.addWidget(current_actions_label)

        self.btnConvertToAutomata = QtWidgets.QPushButton('Conversão para Autômato Finito', self)
        self.btnConvertToAutomata.resize(self.btnConvertToAutomata.sizeHint())
        self.btnConvertToAutomata.clicked.connect(self.convert_to_automata_signal)
        vbox_left.addWidget(self.btnConvertToAutomata)

        btnDeterminize = QtWidgets.QPushButton('Determinizar AF', self)
        btnDeterminize.resize(btnDeterminize.sizeHint())
        btnDeterminize.clicked.connect(self.determinize_automata_signal)
        vbox_left.addWidget(btnDeterminize)

        btnMinimize = QtWidgets.QPushButton('Minimizar AF', self)
        btnMinimize.resize(btnMinimize.sizeHint())
        btnMinimize.clicked.connect(self.minimize_automata_signal)
        vbox_left.addWidget(btnMinimize)

        self.btnGetGrammar = QtWidgets.QPushButton('Converter AF para GR', self)
        self.btnGetGrammar.resize(self.btnGetGrammar.sizeHint())

        # Minimizando o AF antes de gerar a gramática para prevenir crashes
        self.btnGetGrammar.clicked.connect(self.minimize_automata_signal)
        self.btnGetGrammar.clicked.connect(self.get_equivalent_reg_gram_signal)
        vbox_left.addWidget(self.btnGetGrammar)


        sentence_generate_label = QtWidgets.QLabel()
        sentence_generate_label.setText('Geração de sentenças de tamanho n')
        sentence_generate_label.setFont(self.subtitle_font)
        vbox_left.addWidget(sentence_generate_label)
        self.generate_textbox = QtWidgets.QLineEdit()
        self.generate_textbox.setPlaceholderText('Tamanho n (ex: 5)')
        vbox_left.addWidget(self.generate_textbox)
        btn_generate_sentences = QtWidgets.QPushButton('Gerar sentenças', self)
        btn_generate_sentences.resize(btn_generate_sentences.sizeHint())
        btn_generate_sentences.clicked.connect(self.generate_sentences_signal)
        vbox_left.addWidget(btn_generate_sentences)

        sentence_test_label = QtWidgets.QLabel()
        sentence_test_label.setText('Teste de Sentença')
        sentence_test_label.setFont(self.subtitle_font)
        vbox_left.addWidget(sentence_test_label)

        self.textbox = QtWidgets.QLineEdit()
        self.textbox.setPlaceholderText('ex: abba')
        vbox_left.addWidget(self.textbox)

        btn_sentence_test = QtWidgets.QPushButton('Testar', self)
        btn_sentence_test.resize(btn_sentence_test.sizeHint())
        btn_sentence_test.clicked.connect(self.sentence_test_signal)
        vbox_left.addWidget(btn_sentence_test)

        vbox_left.addStretch()


        """
        --------------------------------------------------------
        --------------------------------------------------------
                            * Center Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """

        vbox_center = QtWidgets.QVBoxLayout()
        vbox_center.setSpacing(15)

        """
            Expressão Regular
        """

        self.regex_label = QtWidgets.QLabel()
        self.regex_label.setText('Expressão Regular')
        self.regex_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.regex_label)
        self.regex_label.hide()

        """
            Gramática Regular
        """

        self.grammar_label = QtWidgets.QLabel()
        self.grammar_label.setText('Gramática Regular')
        self.grammar_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.grammar_label)
        self.grammar_label.hide()

        self.initial_panel_label = QtWidgets.QLabel()
        self.initial_panel_label.setText('Para começar, crie/carregue uma Gramática Regular ou Expressão regular')
        self.initial_panel_label.setFont(self.normal_font)
        vbox_center.addWidget(self.initial_panel_label)

        self.table = QtWidgets.QTableWidget(self)
        vbox_center.addWidget(self.table)

        """
            Autômatos Finitos
        """
        self.automata_label = QtWidgets.QLabel()
        self.automata_label.setText('Autômato Finito Equivalente')
        self.automata_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.automata_label)
        self.automata_label.hide()

        self.table_automata = QtWidgets.QTableWidget(self)
        vbox_center.addWidget(self.table_automata)
        self.table_automata.hide()

        self.regex_view = QtWidgets.QLabel()
        self.regex_view.setText('Regex: ')
        self.regex_view.setFont(self.normal_font)
        vbox_center.addWidget(self.regex_view)
        self.regex_view.hide()


        self.generated_sentences_label = QtWidgets.QLabel()
        self.generated_sentences_label.setText('Sentenças Geradas: ')
        self.generated_sentences_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(self.generated_sentences_label)
        self.generated_sentences_label.hide()
        self.table_generated = QtWidgets.QTableWidget(self)
        vbox_center.addWidget(self.table_generated)
        self.table_generated.hide()


        vbox_center.addStretch()

        """
        --------------------------------------------------------
        --------------------------------------------------------
                                                   * Right Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """


        vbox_right = QtWidgets.QVBoxLayout()
        vbox_right.setSpacing(15)

        saved_grammar_label = QtWidgets.QLabel()
        saved_grammar_label.setText('Gramáticas Salvas')
        saved_grammar_label.setFont(self.subtitle_font)
        vbox_right.addWidget(saved_grammar_label)

        self.grammar_list = QtWidgets.QListWidget()
        all_grammar = list(all_reg_grammars.keys())
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox_right.addWidget(self.grammar_list)

        btnRefreshGrammarList = QtWidgets.QPushButton('Atualizar lista', self)
        btnRefreshGrammarList.resize(btnRefreshGrammarList.sizeHint())
        btnRefreshGrammarList.clicked.connect(self.refresh_grammar_list)
        vbox_right.addWidget(btnRefreshGrammarList)

        btnGetGrammar = QtWidgets.QPushButton('Carregar Gramática', self)
        btnGetGrammar.resize(btnGetGrammar.sizeHint())
        btnGetGrammar.clicked.connect(self.get_grammar_from_list)
        vbox_right.addWidget(btnGetGrammar)



        saved_regex_label = QtWidgets.QLabel()
        saved_regex_label.setText('Expressões Regulares Salvas')
        saved_regex_label.setFont(self.subtitle_font)
        vbox_right.addWidget(saved_regex_label)

        self.regex_list = QtWidgets.QListWidget()
        list_all_regex = list(all_regex.keys())
        self.regex_list.addItems(list_all_regex)

        vbox_right.addWidget(self.regex_list)

        btnRefreshRegexList = QtWidgets.QPushButton('Atualizar lista', self)
        btnRefreshRegexList.resize(btnRefreshRegexList.sizeHint())
        btnRefreshRegexList.clicked.connect(self.refresh_regex_list)
        vbox_right.addWidget(btnRefreshRegexList)

        btnGetRegex = QtWidgets.QPushButton('Carregar Expressão Regular', self)
        btnGetRegex.resize(btnGetRegex.sizeHint())
        btnGetRegex.clicked.connect(self.get_regex_from_list)
        vbox_right.addWidget(btnGetRegex)

        vbox_right.addStretch()

        """
            Add Vertical layouts to grid
        """

        grid.addLayout(vbox_left, 0,0)
        grid.setColumnStretch(0,2)
        grid.addLayout(vbox_center, 0,1)
        grid.setColumnStretch(1,6)
        grid.addLayout(vbox_right, 0,2)
        grid.setColumnStretch(2,2)


        self.show()


    def list_grammar_clicked(self,item):
        pass
      # QtWidgets.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

    def create_grammar_signal(self):
        self.grammar_dialog.show()

    def create_regex_signal(self):
        self.regex_dialog.show()

    def refresh_grammar_list(self):
        if os.path.isfile("db/reg_gram.p"):
            all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
            print(list(all_reg_grammars.keys()))
            self.grammar_list.clear()
            # self.grammar_list = QtWidgets.QListWidget()
            all_grammar = list(all_reg_grammars.keys())
            self.grammar_list.addItems(all_grammar)

    def refresh_regex_list(self):
        if os.path.isfile("db/regex.p"):
            all_regex = pickle.load( open( "db/regex.p", "rb" ) )
            print(list(all_regex.keys()))
            self.regex_list.clear()
            # self.regex_list = QtWidgets.QListWidget()
            all_regex = list(all_regex.keys())
            self.regex_list.addItems(all_regex)

    def refresh_grammar(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        data = self.g.G
        initial_state = self.g.initial_state
        print(data)
        if data:
            n_rows = len(list(data.keys()))
            lengths = [len(x) for x in list(data.values())]
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
                    newitem = QtWidgets.QTableWidgetItem(item)
                    newitem.setFont(self.item_font)
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table.setItem(n, m, newitem)

            self.table.setVerticalHeaderLabels(headers)
            for i in range(len(headers)):
                self.table.verticalHeaderItem(i).setFont(self.item_font)
            empty_labels = [" " for x in range(n_cols)]
            self.table.setHorizontalHeaderLabels(empty_labels)
            self.table.resizeColumnsToContents()
            self.table.resizeRowsToContents()

    def get_grammar_from_list(self):
        filename = str(self.grammar_list.currentItem().text())
        if os.path.isfile("db/reg_gram.p"):
            all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
            [self.g.initial_state, self.g.G] = all_reg_grammars[filename]
            self.grammar_label.show()
            self.grammar_label.setText('Gramática Regular: ' + str(filename))
            self.initial_panel_label.setFont(self.item_font)
            self.initial_panel_label.setText('A partir desta Gramática Regular, você pode realizar a conversão para Autômato Finito na barra lateral à esquerda')
            self.regex_view.hide()
            self.table.show()
            self.is_current_a_grammar = True
            # self.btnConvertToAutomata.setFont(self.item_font)
            self.automatas = list()
            self.automata_label.hide()
            self.table_automata.hide()
            self.table_generated.hide()
            self.generated_sentences_label.hide()
            self.refresh_grammar()

    def get_regex_from_list(self):
        if self.regex_list.currentItem():
            filename = str(self.regex_list.currentItem().text())
            if os.path.isfile("db/regex.p"):
                all_regex = pickle.load( open( "db/regex.p", "rb" ) )
                [self.e.literal, self.e.E] = all_regex[filename]
            self.grammar_label.hide()
            self.regex_label.show()
            self.regex_label.setText('Expressão Regular: ' + str(filename))
            self.regex_view.setFont(self.item_font)
            self.initial_panel_label.setFont(self.item_font)
            self.initial_panel_label.setText('A partir desta Expressão Regular, você pode realizar a conversão para Autômato Finito na barra lateral à esquerda')
            self.table.hide()
            self.regex_view.setText(str("Expressão Regular: " + self.e.literal + "\nEstrutura:" + str(self.e.E)))
            self.regex_view.show()
            self.is_current_a_grammar = False
            # self.btnConvertToAutomata.setFont(self.item_font)
            self.automatas = list()
            self.automata_label.hide()
            self.table_automata.hide()
            self.table_generated.hide()
            self.generated_sentences_label.hide()
            self.refresh_grammar()

    def convert_to_automata_signal(self):
        automata = FiniteAutomata()
        if self.is_current_a_grammar:
            automata = self.g.get_eq_automata()
        elif self.e.E:
            automata = self.e.get_equivalent_automata()
        print("automata")
        self.automatas.append(automata)
        self.show_automata()
        self.automata_label.show()
        self.table_automata.show()
        print(automata.pretty_print())

    def determinize_automata_signal(self):
        if len(self.automatas) > 0:
            automata = self.automatas[-1].get_deterministic()
            self.automatas.append(automata)
            self.show_automata()
            self.automata_label.setText("Autômato Finito Determinístico Equivalente")
            self.automata_label.show()
            self.table_automata.show()
            print(automata.pretty_print())

    def minimize_automata_signal(self):
        if len(self.automatas) > 0:
            if self.automatas[-1].is_deterministic:
                automata = self.automatas[-1].get_minimized()
                self.automatas.append(automata)
                self.show_automata()
                self.automata_label.setText("Autômato Finito Determinístico Mínimo Equivalente")
                self.automata_label.show()
                self.table_automata.show()
                print(automata.pretty_print())

    def show_automata(self):
        self.table_automata.setRowCount(0)
        self.table_automata.setColumnCount(0)
        automata = self.automatas[-1]
        transitions = automata.transitions
        initial_state = automata.initial_state
        print(transitions)
        if transitions:
            n_rows = len(automata.K)
            n_cols = len(automata.sigma)

            self.table_automata.setRowCount(n_rows)
            self.table_automata.setColumnCount(n_cols)

            headers = []
            ordered_transitions = sorted(transitions)
            ordered_transitions.remove(initial_state)
            ordered_transitions = [initial_state] + ordered_transitions

            print("ordered_transitions", ordered_transitions)
            print("transitions", transitions)

            for n, key in enumerate(ordered_transitions):
                h = "  " + key
                if key in automata.final_states:
                    h = " *"+key
                headers.append(h)
                for m, item in enumerate(sorted(automata.sigma)):
                    if automata.is_deterministic:
                        newitem = QtWidgets.QTableWidgetItem(transitions[key][item])
                    else:
                        final_string = ""
                        for state in transitions[key][item]:
                            final_string += (state + ",")
                        final_string = final_string[:-1]
                        newitem = QtWidgets.QTableWidgetItem(final_string)
                        newitem.setFont(self.item_font)
                    newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                    self.table_automata.setItem(n, m, newitem)

            headers[0] = "->"+headers[0]
            self.table_automata.setVerticalHeaderLabels(headers)
            for i in range(len(headers)):
                self.table_automata.verticalHeaderItem(i).setFont(self.item_font)
            self.table_automata.setHorizontalHeaderLabels(sorted(automata.sigma))
            self.table_automata.resizeColumnsToContents()
            self.table_automata.resizeRowsToContents()


    def show_automatas(self):
        for automata in self.automatas:
            self.show_automata()

    def sentence_test_signal(self):
        if self.automatas:
            automata = self.automatas[-1]
            sentence = str(self.textbox.text())
            if automata.is_sentence_recognized(sentence):
                QtWidgets.QMessageBox.information(self, "Teste de sentença", "Sua sentença é aceita pelo AF")
            else:
                QtWidgets.QMessageBox.information(self, "Teste de sentença", "Sua sentença NÃO é aceita pelo AF")
        else:
            QtWidgets.QMessageBox.information(self, "Erro", "Você deve gerar o autômato finito equivalente antes disso")


    def generate_sentences_signal(self):
        acceptable = []
        if self.automatas:
            automata = self.automatas[-1]
            size = int(self.generate_textbox.text())
            acceptable = automata.get_acceptable_size_n(size)
        else:
            QtWidgets.QMessageBox.information(self, "Erro", "Você deve gerar o autômato finito equivalente antes disso")

        self.table_generated.setRowCount(0)
        self.table_generated.setColumnCount(0)

        if acceptable:
            n_rows = len(acceptable)
            n_cols = 1

            self.table_generated.setRowCount(n_rows)
            self.table_generated.setColumnCount(n_cols)

            for n, sentence in enumerate(acceptable):
                newitem = QtWidgets.QTableWidgetItem(sentence)
                newitem.setFont(self.item_font)
                newitem.setFlags(QtCore.Qt.ItemIsEnabled)
                self.table_generated.setItem(n, 0, newitem)

            empty_labels = [" " for x in range(n_cols)]
            empty_labels_y = [" " for x in range(n_rows)]
            self.table_generated.setVerticalHeaderLabels(empty_labels_y)
            self.table_generated.setHorizontalHeaderLabels(empty_labels)
            self.table_generated.resizeColumnsToContents()
            self.table_generated.resizeRowsToContents()



        # self.generated_sentences_label.setText(text)
        # self.generated_sentences_label.setFont(self.subtitle_font)
        self.table_generated.show()
        self.generated_sentences_label.show()

    def get_equivalent_reg_gram_signal(self):
        if self.automatas:
            if self.automatas[-1].is_deterministic:
                self.g = self.automatas[-1].get_eq_reg_gram()
                self.table.show()
                self.grammar_label.setText("Gramática Regular equivalente:")
                self.grammar_label.show()
                self.refresh_grammar()




class CreateGrammarWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CreateGrammarWidget, self).__init__()
        self.initUI()
        self.g = RegGram()


    def initUI(self):
        self.setGeometry(75, 75, 800, 800)
        self.setWindowTitle('Gramáticas Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        self.normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        vbox_left = QtWidgets.QVBoxLayout()
        vbox_left.setSpacing(15)
        vbox_center = QtWidgets.QVBoxLayout()
        vbox_center.setSpacing(15)

        vbox_left_label = QtWidgets.QLabel()
        vbox_left_label.setText('Gramáticas Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)

        # gr_name = 'lista2_4a'
        # my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        # print("Initial State: " + str(my_rg.initial_state))
        # print(my_rg.G)

        self.table = QtWidgets.QTableWidget(self)
        vbox_left.addWidget(self.table)

        vbox_left_label = QtWidgets.QLabel()
        vbox_left_label.setText('Ações')
        vbox_left_label.setFont(self.subtitle_2_font)
        vbox_left.addWidget(vbox_left_label)

        production_grid = QtWidgets.QGridLayout()

        self.A_textbox = QtWidgets.QLineEdit()
        self.A_textbox.setPlaceholderText('ex: \"S\"')
        production_grid.addWidget(self.A_textbox, 0,0)

        arrow_label = QtWidgets.QLabel()
        arrow_label.setText('----->')
        arrow_label.setFont(self.title_font)
        production_grid.addWidget(arrow_label, 0,1)

        self.B_textbox = QtWidgets.QLineEdit()
        self.B_textbox.setPlaceholderText('ex: \"aS\"')
        production_grid.addWidget(self.B_textbox, 0,2)

        vbox_left.addLayout(production_grid)

        btnAddRule = QtWidgets.QPushButton('Adicionar regra à produção', self)
        btnAddRule.resize(btnAddRule.sizeHint())
        btnAddRule.clicked.connect(self.signal_add_rule)
        vbox_left.addWidget(btnAddRule)

        btnRemoveRule = QtWidgets.QPushButton('Remover regra da produção', self)
        btnRemoveRule.resize(btnRemoveRule.sizeHint())
        btnRemoveRule.clicked.connect(self.signal_remove_rule)
        vbox_left.addWidget(btnRemoveRule)

        vbox_left.addStretch()

        vbox_center_label = QtWidgets.QLabel()
        vbox_center_label.setText('Salvar Gramática')
        vbox_center_label.setFont(self.subtitle_font)
        vbox_center.addWidget(vbox_center_label)

        filename_label = QtWidgets.QLabel()
        filename_label.setText('Nome do arquivo')
        filename_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(filename_label)

        self.save_textbox = QtWidgets.QLineEdit()
        self.save_textbox.setPlaceholderText('ex: \"gramatica_1\"')
        vbox_center.addWidget(self.save_textbox)

        btn_save_grammar = QtWidgets.QPushButton('Salvar', self)
        btn_save_grammar.resize(btn_save_grammar.sizeHint())
        btn_save_grammar.clicked.connect(self.signal_save_grammar)
        vbox_center.addWidget(btn_save_grammar)

        load_grammar_label = QtWidgets.QLabel()
        load_grammar_label.setText('Carregar nova Gramática')
        load_grammar_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(load_grammar_label)

        self.grammar_list = QtWidgets.QListWidget()
        all_grammar = list(all_reg_grammars.keys())
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox_center.addWidget(self.grammar_list)

        btn_load_grammar = QtWidgets.QPushButton('Carregar', self)
        btn_load_grammar.resize(btn_load_grammar.sizeHint())
        btn_load_grammar.clicked.connect(self.signal_load_grammar)
        vbox_center.addWidget(btn_load_grammar)


        vbox_center.addStretch()

        grid.setColumnStretch(0,3)
        grid.setColumnStretch(1,2)
        grid.addLayout(vbox_left, 0,0)
        grid.addLayout(vbox_center, 0,1)


    def refresh_grammar(self):
        self.table.setRowCount(0)
        self.table.setColumnCount(0)
        data = self.g.G
        initial_state = self.g.initial_state
        print(data)
        if data:
            n_rows = len(list(data.keys()))
            lengths = [len(x) for x in list(data.values())]
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
                    newitem = QtWidgets.QTableWidgetItem(item)
                    newitem.setFont(self.item_font)
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
        if os.path.isfile("db/reg_gram.p"):
            all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
            print(list(all_reg_grammars.keys()))
            self.grammar_list.clear()
            # self.grammar_list = QtWidgets.QListWidget()
            all_grammar = list(all_reg_grammars.keys())
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
            self.B_textbox.setText("")

        else:
            if aux:
                name = aux
                QtWidgets.QMessageBox.information(self, "Erro", name)
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
        print(("Save Grammar: " + str(filename)))
        all_reg_grammars[filename] = [self.g.initial_state, self.g.G]
        pickle.dump(all_reg_grammars, open( "db/reg_gram.p", "wb" ))
        self.refresh_grammar_list()
        QtWidgets.QMessageBox.information(self, 'Salvando', 'Sua gramática \'' + filename + '\' foi salva com sucesso')
        QtWidgets.QMessageBox.information(self, 'Dica', 'Acesse novamente a tela inicial e selecione sua Gramática para manipulações')
        # filenameEntry.delete(0, END)
        return

    """
        Ação de carregar uma gramática salva anteriormente
    """
    def signal_load_grammar(self):
        filename = str(self.grammar_list.currentItem().text())
        if os.path.isfile("db/reg_gram.p"):
            all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
            [self.g.initial_state, self.g.G] = all_reg_grammars[filename]
            self.save_textbox.setText(filename)
            self.refresh_grammar()

        return

    def list_grammar_clicked(self,item):
        pass
        # QtWidgets.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())



class CreateRegexWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(CreateRegexWidget, self).__init__()
        self.initUI()
        self.e = Regex()


    def initUI(self):
        self.setGeometry(75, 75, 800, 800)
        self.setWindowTitle('Expressões Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        self.normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtWidgets.QGridLayout()
        self.setLayout(grid)

        vbox_left = QtWidgets.QVBoxLayout()
        vbox_left.setSpacing(15)
        vbox_center = QtWidgets.QVBoxLayout()
        vbox_center.setSpacing(15)

        vbox_left_label = QtWidgets.QLabel()
        vbox_left_label.setText('Expressões Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)


        self.regex_literal_label = QtWidgets.QLabel()
        self.regex_literal_label.setText('Expressão Regular: __')
        self.regex_literal_label.setFont(self.item_font)
        vbox_left.addWidget(self.regex_literal_label)

        self.regex_e_label = QtWidgets.QLabel()
        self.regex_e_label.setText('Estrutura: __')
        self.regex_e_label.setFont(self.item_font)
        vbox_left.addWidget(self.regex_e_label)

        vbox_left_label = QtWidgets.QLabel()
        vbox_left_label.setText('Ações')
        vbox_left_label.setFont(self.subtitle_2_font)
        vbox_left.addWidget(vbox_left_label)


        self.Exp_textbox = QtWidgets.QLineEdit()
        self.Exp_textbox.setPlaceholderText('ex: \"a(ab|ba)*c?\"')
        vbox_left.addWidget(self.Exp_textbox)


        btnAddRule = QtWidgets.QPushButton('Atribuir Expressão Regular', self)
        btnAddRule.resize(btnAddRule.sizeHint())
        btnAddRule.clicked.connect(self.signal_set_regex)
        vbox_left.addWidget(btnAddRule)

        vbox_left.addStretch()

        vbox_center_label = QtWidgets.QLabel()
        vbox_center_label.setText('Salvar Expressão Regular')
        vbox_center_label.setFont(self.subtitle_font)
        vbox_center.addWidget(vbox_center_label)

        filename_label = QtWidgets.QLabel()
        filename_label.setText('Nome do arquivo')
        filename_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(filename_label)

        self.save_textbox = QtWidgets.QLineEdit()
        self.save_textbox.setPlaceholderText('ex: \"regex_1\"')
        vbox_center.addWidget(self.save_textbox)

        btn_save_regex = QtWidgets.QPushButton('Salvar', self)
        btn_save_regex.resize(btn_save_regex.sizeHint())
        btn_save_regex.clicked.connect(self.signal_save_regex)
        vbox_center.addWidget(btn_save_regex)

        load_regex_label = QtWidgets.QLabel()
        load_regex_label.setText('Carregar nova Expressão Reg.')
        load_regex_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(load_regex_label)

        self.regex_list = QtWidgets.QListWidget()
        all_reg = list(all_regex.keys())
        self.regex_list.addItems(all_reg)
        self.regex_list.itemClicked.connect(self.list_regex_clicked)

        vbox_center.addWidget(self.regex_list)

        btn_load_regex = QtWidgets.QPushButton('Carregar', self)
        btn_load_regex.resize(btn_load_regex.sizeHint())
        btn_load_regex.clicked.connect(self.signal_load_regex)
        vbox_center.addWidget(btn_load_regex)


        vbox_center.addStretch()

        grid.setColumnStretch(0,3)
        grid.setColumnStretch(1,2)
        grid.addLayout(vbox_left, 0,0)
        grid.addLayout(vbox_center, 0,1)


    def refresh_regex(self):
        self.regex_literal_label.setText(str("Expressão Regular: " + self.e.literal))
        self.regex_e_label.setText(str("Estrutura: " + str(self.e.E)))


    def refresh_regex_list(self):
        if os.path.isfile("db/regex.p"):
            all_regex = pickle.load( open( "db/regex.p", "rb" ) )
            print(list(all_regex.keys()))
            self.regex_list.clear()
            # self.regex_list = QtWidgets.QListWidget()
            all_regex = list(all_regex.keys())
            self.regex_list.addItems(all_regex)

    """
        Ação de adicionar regra numa gramática regular
    """
    def signal_set_regex(self):
        print("tão")
        exp = str(self.Exp_textbox.text())
        print(exp)
        aux = self.e.set_regex(exp)
        self.refresh_regex()
        print(aux)
        return


    """
        Ação de salvar a gramática em arquivo "filename"
    """
    def signal_save_regex(self):
        filename = str(self.save_textbox.text())
        print(("Save Regex: " + str(filename)))
        all_regex[filename] = [self.e.literal, self.e.E]
        pickle.dump(all_regex, open( "db/regex.p", "wb" ))
        self.refresh_regex_list()
        QtWidgets.QMessageBox.information(self, 'Salvando', 'Sua exp. regular \''+ filename  + '\' foi salva com sucesso')
        QtWidgets.QMessageBox.information(self, 'Dica', 'Acesse novamente a tela inicial e selecione sua Expressão para manipulações')
        # filenameEntry.delete(0, END)
        return

    """
        Ação de carregar uma gramática salva anteriormente
    """
    def signal_load_regex(self):
        if self.regex_list.currentItem():
            filename = str(self.regex_list.currentItem().text())
            if os.path.isfile("db/regex.p"):
                all_regex = pickle.load( open( "db/regex.p", "rb" ) )
                [self.e.literal, self.e.E] = all_regex[filename]
                self.refresh_regex()
                self.Exp_textbox.setText(self.e.literal)
                self.save_textbox.setText(filename)
        return

    def list_regex_clicked(self,item):
        pass
        # QtWidgets.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())



def main():
    app = QtWidgets.QApplication(sys.argv)
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
