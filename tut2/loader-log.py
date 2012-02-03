import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

from webpage import WebPage

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.view = QWebView(self)
        self.view.setPage(WebPage())

        layout = QVBoxLayout(self)
        layout.setMargin(0)
        layout.addWidget(self.view)

def main():
    app = QApplication(sys.argv)
    window = Window()
    html = open(sys.argv[1]).read()
    window.show()
    window.view.setHtml(html)
    app.exec_()

if __name__ == "__main__":
    main()
