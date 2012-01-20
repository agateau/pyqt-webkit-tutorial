import os
import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        view = QWebView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(view)

        pyDir = os.path.abspath(os.path.dirname(__file__))
        baseUrl = QUrl.fromLocalFile(os.path.join(pyDir, "static/"))
        html = """
            <html><body>
            <div>Hello World!</div>
            <img src="test.png"/>
            </body></html>
            """
        view.setHtml(html, baseUrl)

def main():
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()

if __name__ == "__main__":
    main()
