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

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        """
        --------------------------------------------------------
        --------------------------------------------------------
        * Left Panel
        --------------------------------------------------------
        --------------------------------------------------------
        """

        vbox_left = QtGui.QVBoxLayout()
        vbox_left.setSpacing(15)

        vbox_left_label = QtGui.QLabel()
        vbox_left_label.setText(u'Linguagens Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)

        self.grammar_dialog = CreateGrammarWidget(self)

        btnCreateGrammar = QtGui.QPushButton(u'Criar/Editar Gramática Regular', self)
        btnCreateGrammar.resize(btnCreateGrammar.sizeHint())
        btnCreateGrammar.clicked.connect(self.create_grammar_signal)
        vbox_left.addWidget(btnCreateGrammar)

        self.regex_dialog = CreateRegexWidget(self)

        btnCreateRegex = QtGui.QPushButton(u'Criar/Editar Expressão Regular', self)
        btnCreateRegex.resize(btnCreateRegex.sizeHint())
        btnCreateRegex.clicked.connect(self.create_regex_signal)
        vbox_left.addWidget(btnCreateRegex)

        current_actions_label = QtGui.QLabel()
        current_actions_label.setText(u'Ações com o modelo atual')
        current_actions_label.setFont(self.subtitle_font)
        vbox_left.addWidget(current_actions_label)

        self.btnConvertToAutomata = QtGui.QPushButton(u'Conversão para Autômato Finito', self)
        self.btnConvertToAutomata.resize(self.btnConvertToAutomata.sizeHint())
        self.btnConvertToAutomata.clicked.connect(self.convert_to_automata_signal)
        vbox_left.addWidget(self.btnConvertToAutomata)

        btnDeterminize = QtGui.QPushButton(u'Determinizar AF', self)
        btnDeterminize.resize(btnDeterminize.sizeHint())
        btnDeterminize.clicked.connect(self.determinize_automata_signal)
        vbox_left.addWidget(btnDeterminize)

        btnMinimize = QtGui.QPushButton(u'Minimizar AF', self)
        btnMinimize.resize(btnMinimize.sizeHint())
        btnMinimize.clicked.connect(self.minimize_automata_signal)
        vbox_left.addWidget(btnMinimize)

        self.btnGetGrammar = QtGui.QPushButton(u'Converter AF para GR', self)
        self.btnGetGrammar.resize(self.btnGetGrammar.sizeHint())
        self.btnGetGrammar.clicked.connect(self.get_equivalent_reg_gram_signal)
        vbox_left.addWidget(self.btnGetGrammar)


        sentence_generate_label = QtGui.QLabel()
        sentence_generate_label.setText(u'Geração de sentenças de tamanho n')
        sentence_generate_label.setFont(self.subtitle_font)
        vbox_left.addWidget(sentence_generate_label)
        self.generate_textbox = QtGui.QLineEdit()
        self.generate_textbox.setPlaceholderText(u'Tamanho n (ex: 5)')
        vbox_left.addWidget(self.generate_textbox)
        btn_generate_sentences = QtGui.QPushButton(u'Gerar sentenças', self)
        btn_generate_sentences.resize(btn_generate_sentences.sizeHint())
        btn_generate_sentences.clicked.connect(self.generate_sentences_signal)
        vbox_left.addWidget(btn_generate_sentences)

        sentence_test_label = QtGui.QLabel()
        sentence_test_label.setText(u'Teste de Sentença')
        sentence_test_label.setFont(self.subtitle_font)
        vbox_left.addWidget(sentence_test_label)

        self.textbox = QtGui.QLineEdit()
        self.textbox.setPlaceholderText(u'ex: abba')
        vbox_left.addWidget(self.textbox)

        btn_sentence_test = QtGui.QPushButton('Testar', self)
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

        vbox_center = QtGui.QVBoxLayout()
        vbox_center.setSpacing(15)

        """
            Expressão Regular
        """

        self.regex_label = QtGui.QLabel()
        self.regex_label.setText(u'Expressão Regular')
        self.regex_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.regex_label)
        self.regex_label.hide()

        """
            Gramática Regular
        """

        self.grammar_label = QtGui.QLabel()
        self.grammar_label.setText(u'Gramática Regular')
        self.grammar_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.grammar_label)
        self.grammar_label.hide()

        self.initial_panel_label = QtGui.QLabel()
        self.initial_panel_label.setText(u'Para começar, crie/carregue uma Gramática Regular ou Expressão regular')
        self.initial_panel_label.setFont(self.normal_font)
        vbox_center.addWidget(self.initial_panel_label)

        self.table = QtGui.QTableWidget(self)
        vbox_center.addWidget(self.table)

        """
            Autômatos Finitos
        """
        self.automata_label = QtGui.QLabel()
        self.automata_label.setText(u'Autômato Finito Equivalente')
        self.automata_label.setFont(self.subtitle_font)
        vbox_center.addWidget(self.automata_label)
        self.automata_label.hide()

        self.table_automata = QtGui.QTableWidget(self)
        vbox_center.addWidget(self.table_automata)
        self.table_automata.hide()

        self.regex_view = QtGui.QLabel()
        self.regex_view.setText(u'Regex: ')
        self.regex_view.setFont(self.normal_font)
        vbox_center.addWidget(self.regex_view)
        self.regex_view.hide()


        self.generated_sentences_label = QtGui.QLabel()
        self.generated_sentences_label.setText(u'Sentenças Geradas: ')
        self.generated_sentences_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(self.generated_sentences_label)
        self.generated_sentences_label.hide()
        self.table_generated = QtGui.QTableWidget(self)
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


        vbox_right = QtGui.QVBoxLayout()
        vbox_right.setSpacing(15)

        saved_grammar_label = QtGui.QLabel()
        saved_grammar_label.setText(u'Gramáticas Salvas')
        saved_grammar_label.setFont(self.subtitle_font)
        vbox_right.addWidget(saved_grammar_label)

        self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox_right.addWidget(self.grammar_list)

        btnRefreshGrammarList = QtGui.QPushButton(u'Atualizar lista', self)
        btnRefreshGrammarList.resize(btnRefreshGrammarList.sizeHint())
        btnRefreshGrammarList.clicked.connect(self.refresh_grammar_list)
        vbox_right.addWidget(btnRefreshGrammarList)

        btnGetGrammar = QtGui.QPushButton(u'Carregar Gramática', self)
        btnGetGrammar.resize(btnGetGrammar.sizeHint())
        btnGetGrammar.clicked.connect(self.get_grammar_from_list)
        vbox_right.addWidget(btnGetGrammar)



        saved_regex_label = QtGui.QLabel()
        saved_regex_label.setText(u'Expressões Regulares Salvas')
        saved_regex_label.setFont(self.subtitle_font)
        vbox_right.addWidget(saved_regex_label)

        self.regex_list = QtGui.QListWidget()
        list_all_regex = all_regex.keys()
        self.regex_list.addItems(list_all_regex)

        vbox_right.addWidget(self.regex_list)

        btnRefreshRegexList = QtGui.QPushButton(u'Atualizar lista', self)
        btnRefreshRegexList.resize(btnRefreshRegexList.sizeHint())
        btnRefreshRegexList.clicked.connect(self.refresh_regex_list)
        vbox_right.addWidget(btnRefreshRegexList)

        btnGetRegex = QtGui.QPushButton(u'Carregar Expressão Regular', self)
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
      # QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())

    def create_grammar_signal(self):
        self.grammar_dialog.show()

    def create_regex_signal(self):
        self.regex_dialog.show()

    def refresh_grammar_list(self):
        if os.path.isfile("db/reg_gram.p"):
            all_reg_grammars = pickle.load(open( "db/reg_gram.p", "rb" ))
            print all_reg_grammars.keys()
            self.grammar_list.clear()
            # self.grammar_list = QtGui.QListWidget()
            all_grammar = all_reg_grammars.keys()
            self.grammar_list.addItems(all_grammar)

    def refresh_regex_list(self):
        if os.path.isfile("db/regex.p"):
            all_regex = pickle.load( open( "db/regex.p", "rb" ) )
            print all_regex.keys()
            self.regex_list.clear()
            # self.regex_list = QtGui.QListWidget()
            all_regex = all_regex.keys()
            self.regex_list.addItems(all_regex)

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
            self.grammar_label.setText(u'Gramática Regular: ' + str(filename))
            self.initial_panel_label.setFont(self.item_font)
            self.initial_panel_label.setText(u'A partir desta Gramática Regular, você pode realizar a conversão para Autômato Finito na barra lateral à esquerda')
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
            self.regex_label.setText(u'Expressão Regular: ' + str(filename))
            self.regex_view.setFont(self.item_font)
            self.initial_panel_label.setFont(self.item_font)
            self.initial_panel_label.setText(u'A partir desta Expressão Regular, você pode realizar a conversão para Autômato Finito na barra lateral à esquerda')
            self.table.hide()
            self.regex_view.setText(str("Expressão Regular: " + self.e.literal + "\nEstrutura:" + str(self.e.E)).decode("utf-8"))
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
        print "automata"
        self.automatas.append(automata)
        self.show_automata()
        self.automata_label.show()
        self.table_automata.show()
        print automata.pretty_print()

    def determinize_automata_signal(self):
        automata = self.automatas[-1].get_deterministic()
        self.automatas.append(automata)
        self.show_automata()
        self.automata_label.setText(u"Autômato Finito Determinístico Equivalente")
        self.automata_label.show()
        self.table_automata.show()
        print automata.pretty_print()

    def minimize_automata_signal(self):
        if self.automatas[-1].is_deterministic:
            automata = self.automatas[-1].get_minimized()
            self.automatas.append(automata)
            self.show_automata()
            self.automata_label.setText(u"Autômato Finito Determinístico Mínimo Equivalente")
            self.automata_label.show()
            self.table_automata.show()
            print automata.pretty_print()

    def show_automata(self):
        self.table_automata.setRowCount(0)
        self.table_automata.setColumnCount(0)
        automata = self.automatas[-1]
        transitions = automata.transitions
        initial_state = automata.initial_state
        print transitions
        if transitions:
            n_rows = len(automata.K)
            n_cols = len(automata.sigma)

            self.table_automata.setRowCount(n_rows)
            self.table_automata.setColumnCount(n_cols)

            headers = []
            ordered_transitions = sorted(transitions)
            ordered_transitions.remove(initial_state)
            ordered_transitions = [initial_state] + ordered_transitions

            print "ordered_transitions", ordered_transitions
            print "transitions", transitions

            for n, key in enumerate(ordered_transitions):
                h = "  " + key
                if key in automata.final_states:
                    h = " *"+key
                headers.append(h)
                for m, item in enumerate(sorted(automata.sigma)):
                    if automata.is_deterministic:
                        newitem = QtGui.QTableWidgetItem(transitions[key][item])
                    else:
                        final_string = ""
                        for state in transitions[key][item]:
                            final_string += (state + ",")
                        final_string = final_string[:-1]
                        newitem = QtGui.QTableWidgetItem(final_string)
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
                QtGui.QMessageBox.information(self, u"Teste de sentença", u"Sua sentença é aceita pelo AF")
            else:
                QtGui.QMessageBox.information(self, u"Teste de sentença", u"Sua sentença NÃO é aceita pelo AF")
        else:
            QtGui.QMessageBox.information(self, u"Erro", u"Você deve gerar o autômato finito equivalente antes disso")


    def generate_sentences_signal(self):
        acceptable = []
        if self.automatas:
            automata = self.automatas[-1]
            size = int(self.generate_textbox.text())
            acceptable = automata.get_acceptable_size_n(size)
        else:
            QtGui.QMessageBox.information(self, u"Erro", u"Você deve gerar o autômato finito equivalente antes disso")

        self.table_generated.setRowCount(0)
        self.table_generated.setColumnCount(0)

        if acceptable:
            n_rows = len(acceptable)
            n_cols = 1

            self.table_generated.setRowCount(n_rows)
            self.table_generated.setColumnCount(n_cols)

            for n, sentence in enumerate(acceptable):
                newitem = QtGui.QTableWidgetItem(sentence)
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
                self.grammar_label.setText(u"Gramática Regular equivalente:")
                self.grammar_label.show()
                self.refresh_grammar()




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
        self.normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        vbox_left = QtGui.QVBoxLayout()
        vbox_left.setSpacing(15)
        vbox_center = QtGui.QVBoxLayout()
        vbox_center.setSpacing(15)

        vbox_left_label = QtGui.QLabel()
        vbox_left_label.setText(u'Gramáticas Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)

        # gr_name = 'lista2_4a'
        # my_rg = RegGram(all_reg_grammars[gr_name][1],all_reg_grammars[gr_name][0])
        # print("Initial State: " + str(my_rg.initial_state))
        # print(my_rg.G)

        self.table = QtGui.QTableWidget(self)
        vbox_left.addWidget(self.table)

        vbox_left_label = QtGui.QLabel()
        vbox_left_label.setText(u'Ações')
        vbox_left_label.setFont(self.subtitle_2_font)
        vbox_left.addWidget(vbox_left_label)

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

        vbox_left.addLayout(production_grid)

        btnAddRule = QtGui.QPushButton(u'Adicionar regra à produção', self)
        btnAddRule.resize(btnAddRule.sizeHint())
        btnAddRule.clicked.connect(self.signal_add_rule)
        vbox_left.addWidget(btnAddRule)

        btnRemoveRule = QtGui.QPushButton(u'Remover regra da produção', self)
        btnRemoveRule.resize(btnRemoveRule.sizeHint())
        btnRemoveRule.clicked.connect(self.signal_remove_rule)
        vbox_left.addWidget(btnRemoveRule)

        vbox_left.addStretch()

        vbox_center_label = QtGui.QLabel()
        vbox_center_label.setText(u'Salvar Gramática')
        vbox_center_label.setFont(self.subtitle_font)
        vbox_center.addWidget(vbox_center_label)

        filename_label = QtGui.QLabel()
        filename_label.setText(u'Nome do arquivo')
        filename_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(filename_label)

        self.save_textbox = QtGui.QLineEdit()
        self.save_textbox.setPlaceholderText(u'ex: \"gramatica_1\"')
        vbox_center.addWidget(self.save_textbox)

        btn_save_grammar = QtGui.QPushButton(u'Salvar', self)
        btn_save_grammar.resize(btn_save_grammar.sizeHint())
        btn_save_grammar.clicked.connect(self.signal_save_grammar)
        vbox_center.addWidget(btn_save_grammar)

        load_grammar_label = QtGui.QLabel()
        load_grammar_label.setText(u'Carregar nova Gramática')
        load_grammar_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(load_grammar_label)

        self.grammar_list = QtGui.QListWidget()
        all_grammar = all_reg_grammars.keys()
        self.grammar_list.addItems(all_grammar)
        self.grammar_list.itemClicked.connect(self.list_grammar_clicked)

        vbox_center.addWidget(self.grammar_list)

        btn_load_grammar = QtGui.QPushButton(u'Carregar', self)
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
            self.B_textbox.setText("")

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
        QtGui.QMessageBox.information(self, u'Salvando', u'Sua gramática \'' + filename + u'\' foi salva com sucesso')
        QtGui.QMessageBox.information(self, u'Dica', u'Acesse novamente a tela inicial e selecione sua Gramática para manipulações')
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
        # QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())



class CreateRegexWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(CreateRegexWidget, self).__init__()
        self.initUI()
        self.e = Regex()


    def initUI(self):
        self.setGeometry(75, 75, 800, 800)
        self.setWindowTitle(u'Expressões Regulares')

        self.title_font = QtGui.QFont("Arial", 24, QtGui.QFont.Bold)
        self.subtitle_font = QtGui.QFont("Arial", 20, QtGui.QFont.Bold)
        self.subtitle_2_font = QtGui.QFont("Arial", 18, QtGui.QFont.Bold)
        self.normal_font = QtGui.QFont("Arial", 16, QtGui.QFont.Normal)
        self.item_font = QtGui.QFont("Arial", 14, QtGui.QFont.Normal)

        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        vbox_left = QtGui.QVBoxLayout()
        vbox_left.setSpacing(15)
        vbox_center = QtGui.QVBoxLayout()
        vbox_center.setSpacing(15)

        vbox_left_label = QtGui.QLabel()
        vbox_left_label.setText(u'Expressões Regulares')
        vbox_left_label.setFont(self.title_font)
        vbox_left.addWidget(vbox_left_label)


        self.regex_literal_label = QtGui.QLabel()
        self.regex_literal_label.setText(u'Expressão Regular: __')
        self.regex_literal_label.setFont(self.item_font)
        vbox_left.addWidget(self.regex_literal_label)

        self.regex_e_label = QtGui.QLabel()
        self.regex_e_label.setText(u'Estrutura: __')
        self.regex_e_label.setFont(self.item_font)
        vbox_left.addWidget(self.regex_e_label)

        vbox_left_label = QtGui.QLabel()
        vbox_left_label.setText(u'Ações')
        vbox_left_label.setFont(self.subtitle_2_font)
        vbox_left.addWidget(vbox_left_label)


        self.Exp_textbox = QtGui.QLineEdit()
        self.Exp_textbox.setPlaceholderText(u'ex: \"a(ab|ba)*c?\"')
        vbox_left.addWidget(self.Exp_textbox)


        btnAddRule = QtGui.QPushButton(u'Atribuir Expressão Regular', self)
        btnAddRule.resize(btnAddRule.sizeHint())
        btnAddRule.clicked.connect(self.signal_set_regex)
        vbox_left.addWidget(btnAddRule)

        vbox_left.addStretch()

        vbox_center_label = QtGui.QLabel()
        vbox_center_label.setText(u'Salvar Expressão Regular')
        vbox_center_label.setFont(self.subtitle_font)
        vbox_center.addWidget(vbox_center_label)

        filename_label = QtGui.QLabel()
        filename_label.setText(u'Nome do arquivo')
        filename_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(filename_label)

        self.save_textbox = QtGui.QLineEdit()
        self.save_textbox.setPlaceholderText(u'ex: \"regex_1\"')
        vbox_center.addWidget(self.save_textbox)

        btn_save_regex = QtGui.QPushButton(u'Salvar', self)
        btn_save_regex.resize(btn_save_regex.sizeHint())
        btn_save_regex.clicked.connect(self.signal_save_regex)
        vbox_center.addWidget(btn_save_regex)

        load_regex_label = QtGui.QLabel()
        load_regex_label.setText(u'Carregar nova Expressão Reg.')
        load_regex_label.setFont(self.subtitle_2_font)
        vbox_center.addWidget(load_regex_label)

        self.regex_list = QtGui.QListWidget()
        all_reg = all_regex.keys()
        self.regex_list.addItems(all_reg)
        self.regex_list.itemClicked.connect(self.list_regex_clicked)

        vbox_center.addWidget(self.regex_list)

        btn_load_regex = QtGui.QPushButton(u'Carregar', self)
        btn_load_regex.resize(btn_load_regex.sizeHint())
        btn_load_regex.clicked.connect(self.signal_load_regex)
        vbox_center.addWidget(btn_load_regex)


        vbox_center.addStretch()

        grid.setColumnStretch(0,3)
        grid.setColumnStretch(1,2)
        grid.addLayout(vbox_left, 0,0)
        grid.addLayout(vbox_center, 0,1)


    def refresh_regex(self):
        self.regex_literal_label.setText(str("Expressão Regular: " + self.e.literal).decode("utf-8"))
        self.regex_e_label.setText(str("Estrutura: " + str(self.e.E)).decode("utf-8"))


    def refresh_regex_list(self):
        if os.path.isfile("db/regex.p"):
            all_regex = pickle.load( open( "db/regex.p", "rb" ) )
            print all_regex.keys()
            self.regex_list.clear()
            # self.regex_list = QtGui.QListWidget()
            all_regex = all_regex.keys()
            self.regex_list.addItems(all_regex)

    """
        Ação de adicionar regra numa gramática regular
    """
    def signal_set_regex(self):
        print "tão"
        exp = str(self.Exp_textbox.text())
        print exp
        aux = self.e.set_regex(exp)
        self.refresh_regex()
        print aux
        # if aux == True:
        #     self.refresh_regex()
        # else:
        #     if aux:
        #         name = aux.decode("utf-8")
        #         QtGui.QMessageBox.information(self, "Erro", name)
        # # newEntry2.delete(0, END)
        return


    """
        Ação de salvar a gramática em arquivo "filename"
    """
    def signal_save_regex(self):
        filename = str(self.save_textbox.text())
        print("Save Regex: " + str(filename))
        all_regex[filename] = [self.e.literal, self.e.E]
        pickle.dump(all_regex, open( "db/regex.p", "wb" ))
        self.refresh_regex_list()
        QtGui.QMessageBox.information(self, u'Salvando', u'Sua exp. regular \''+ filename.decode("utf-8")  + u'\' foi salva com sucesso')
        QtGui.QMessageBox.information(self, u'Dica', u'Acesse novamente a tela inicial e selecione sua Expressão para manipulações')
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
        # QtGui.QMessageBox.information(self, "ListWidget", "You clicked: "+item.text())



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
