import sys
from PyQt4 import QtGui


class PrettyWidget(QtGui.QWidget):

    def __init__(self):
        super(PrettyWidget, self).__init__()
        self.initUI()


    def initUI(self):
        self.setGeometry(600, 300, 400, 200)
        self.setWindowTitle('Signals and Events')

        self.btn = QtGui.QPushButton('Button', self)
        self.btn.resize(self.btn.sizeHint())
        self.btn.move(150, 100)
        self.btn.clicked.connect(self.Signal)

        self.lbl = QtGui.QLabel(self)
        self.lbl.move(180, 50)
        self.lbl.setText('Slot')
        self.lbl.adjustSize()

        self.show()

    def Signal(self):
        self.lbl.setText('Signal Received')
        self.lbl.move(150, 50)
        self.lbl.adjustSize()

def main():
    app = QtGui.QApplication(sys.argv)
    w = PrettyWidget()
    app.exec_()


if __name__ == '__main__':
    main()
