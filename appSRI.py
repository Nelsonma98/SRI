import sys
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from model import Model
from vectorial_model import VectorialModel
from boolean_model import BooleanModel
from fuzzy import FuzzyModel
from corpus import Corpus
from constants import *


class App_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('appSRI.ui', self)

        self.corpusCran = Corpus(CRAN_CORPUS_NAME)
        self.corpusMed = Corpus(MED_CORPUS_NAME)

        self.vc = VectorialModel(self.corpusCran)
        self.bc = BooleanModel(self.corpusCran)
        self.fc = FuzzyModel(self.corpusCran)

        self.vm = VectorialModel(self.corpusMed)
        self.bm = BooleanModel(self.corpusMed)
        self.fm = FuzzyModel(self.corpusMed)

        self.type_model = VEC_MODEL_NAME
        self.name_corpus = CRAN_CORPUS_NAME

        self.Vectorial_3.setChecked(True)
        self.Cran_3.setChecked(True)

        self.Vectorial_3.clicked.connect(self.check_vectorial)
        self.Booleano_3.clicked.connect(self.check_booleano)
        self.Fuzzy_3.clicked.connect(self.check_fuzzy)

        self.Cran_3.clicked.connect(self.check_cran)
        self.Med_3.clicked.connect(self.check_med)

        self.Aceptar.clicked.connect(self.create_model)

        self.Buscar.clicked.connect(self.process_query)
        
        self.Atras.clicked.connect(self.ir_atras)
    
    def check_vectorial(self):
        if self.Vectorial_3.isChecked():
            self.type_model = VEC_MODEL_NAME
    
    def check_booleano(self):
        if self.Booleano_3.isChecked():
            self.type_model = BOOL_MODEL_NAME

    def check_fuzzy(self):
        if self.Fuzzy_3.isChecked():
            self.type_model = FUZZY_MODEL_NAME

    def check_cran(self):
        if self.Cran_3.isChecked():
            self.name_corpus = CRAN_CORPUS_NAME

    def check_med(self):
        if self.Med_3.isChecked():
            self.name_corpus = MED_CORPUS_NAME

    def create_model(self):
        self.stackedWidget.setCurrentWidget(self.page)
    
    def process_query(self):
        query = self.textEdit.toPlainText()

        if self.type_model == VEC_MODEL_NAME and self.name_corpus == CRAN_CORPUS_NAME:
            result = self.vc.similarity(query)
        elif self.type_model == VEC_MODEL_NAME and self.name_corpus == MED_CORPUS_NAME:
            result = self.vm.similarity(query)
        elif self.type_model == BOOL_MODEL_NAME and self.name_corpus == CRAN_CORPUS_NAME:
            result = self.bc.similarity(query)
        elif self.type_model == BOOL_MODEL_NAME and self.name_corpus == MED_CORPUS_NAME:
            result = self.bm.similarity(query)
        elif self.type_model == FUZZY_MODEL_NAME and self.name_corpus == MED_CORPUS_NAME:
            result = self.fm.similarity(query)
        else:
            result = self.fc.similarity(query)
        
        self.show_results(result)
    
    def show_results(self, results):
        self.vbox = QVBoxLayout()

        for _,result in results:
            label = QLabel(result)
            label.setMinimumSize(0, 50)
            label.setMaximumSize(1200, 50)
            self.vbox.addWidget(label)

        self.widget = QWidget()
        self.widget.setLayout(self.vbox)
        self.scrollArea_2.setWidget(self.widget)

    def ir_atras(self):
        self.stackedWidget.setCurrentWidget(self.inicio)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = App_GUI()
    gui.show()
    sys.exit(app.exec_())