import sys
from PyQt5.Qt import QApplication, QClipboard
from PyQt5 import QtCore, QtWidgets, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QPlainTextEdit
from PyQt5.QtCore import QSize
from PyQt5 import QtWidgets

class ExampleWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(440, 240))    
        self.setWindowTitle("PyQt5 Clipboard example") 
        
        # Add text field
        self.b = QPlainTextEdit(self)
        self.b.insertPlainText("Use your mouse to copy text to the clipboard.\nText can be copied from any application.\n")
        self.b.move(10,10)
        self.b.resize(400,200)

        # QApplication.clipboard().dataChanged.connect(self.clipboardChanged)
        QtWidgets.QApplication.clipboard().dataChanged.connect(self.clipboardChanged)

    # Get the system clipboard contents
    def clipboardChanged(self):
        # text = QApplication.clipboard().text()
        text = QtWidgets.QApplication.clipboard().text()
        print(text)
        self.b.insertPlainText(text + '\n')

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWin = ExampleWindow()
    mainWin.show()
    sys.exit( app.exec_() )