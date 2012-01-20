import sys

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtWebKit import *

class Foo(QObject):
    @pyqtSlot(int, result=int)
    def compute(self, value):
        return value * 2

    @pyqtSlot()
    def quit(self):
        QApplication.quit()

class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        view = QWebView(self)
        layout = QVBoxLayout(self)
        layout.addWidget(view)

        self.foo = Foo(self)
        view.page().mainFrame().addToJavaScriptWindowObject("foo", self.foo)

        view.setHtml("""
        <html>
        <script>
        function updateEntry() {
            var element = document.getElementById("entry");
            var result = foo.compute(element.value);
            element.value = result;
        }
        </script>
        <body>
        <div>
            <input type="text" id="entry"/>
            <input type="button" value="Compute" onclick="updateEntry()"/>
        </div>
        <div>
            <input type="button" value="Quit" onclick="foo.quit()"/>
        </div>
        </body>
        </html>
        """)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
