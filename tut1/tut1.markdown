# Swimming against the stream or preparing for next stream change? HTML+PyQt experiment

----

It is an interesting time to be a Qt developer: new ways to develop applications are emerging, one can either ignore them or experiment... I like experimentations.

In one corner we have traditional, QWidget-based Qt development.

In another corner we have QML, a declarative language coupled with JavaScript, which brings a whole new way to think about application development. Qt developers are betting a lot on QML, planning for it to be the preferred way to develop new applications with Qt 5.

In yet another corner is the Web, a perfect demonstration of technology hijacking: what was once designed to present structured documents has become one of the most powerful way to create applications.

Of those three technologies, I believe QML is the most innovative and powerful one, and I had high hopes it could secure a significant market share when Nokia and Intel were still planning to deliver it on their upcoming smart-phones and tablets. Now that Nokia switched to WP7 and Intel switched to EFL, I am a lot less confident QML will succeed. Experience shows that when two technologies are in competition, the best one does not automatically wins, parameters like market share and learning curve are as important as, if not more important than, technical excellence.

Not willing to ignore the behemoth that is the Web, I started an experiment: how would it feel to develop an application which would mix Qt and HTML rendering? Thanks to QtWebKit, this kind of integration is easy to achieve. My experimentation subject is based on <a href="http://yokadi.github.com">Yokadi</a>, a command-line based TODO list I work on. I decided to create a graphical frontend for it. The result is this:

![QYok due page](qyok1.png)
![QYok projects page](qyok2.png)

This application, named <a href="http://github.com/agateau/qyok">QYok</a> (yes, I suck at naming applications, suggestions for better names are welcome!), is an interesting mix of technologies. It uses:

- <a href="http://www.riverbankcomputing.com/software/pyqt/">PyQt</a>, for the main window and most of the widgets
- <a href="http://trac.webkit.org/wiki/QtWebKit">QtWebKit</a>, to display the task lists
- <a href="http://jquery.com">jQuery</a>, to make it easier to manipulate the HTML and provide nice animations
- <a href="http://jinja.pocoo.org/">Jinja2</a>, a Python-based template system, using a syntax similar to Django (and thus Grantlee)
- and of course, Yokadi itself, to provide access to the application data

# Getting a Qt application to show HTML code

This is the first, very easy, step. Here is a complete example:



I hit my first little road-block here: the HTML code contained references to images stored in a "static" dir alongside the Python code, but I couldn't get the images to appear. setHtml() has a second optional parameter which defines the base url for all relative paths specified in the HTML. I thus called setHtml() like this: `webView.setHtml(html, baseUrl)`, where baseUrl was defined as "/my/python/code/static" but that didn't work. After quite some head scratching, I figured it out: baseUrl must end with a trailing slash. Tricky.

# Calling Qt code from JavaScript

QWebView.setHtml() makes it easy for Qt code to provide HTML content to WebKit, but it is a one-way only setup: it doesn't provide a way for JavaScript code to call Qt code. The way to do this is by exposing objects created on the Qt side to QWebView (or more precisely, to the main frame of the QWebPage inside QWebView).

QtWebKit takes advantage of Qt introspection features to access object methods and properties. To be exposed to JavaScript, an object must thus inherit from QObject and expose itself through Qt properties, Qt signals and Qt slots. Here is an example. First lets define a class named Foo which implements a compute() slot, performing complicated computations and a quit() slot:

    class Foo(QObject):
        @pyqtSlot(int, result=int)
        def compute(self, value):
            return value * 2

        @pyqtSlot()
        def quit(self):
            QApplication.quit()

The important part here are the "@pyqtSlot()" decorators, which take care of turning our methods into slots. As you may have guessed, the decorator expect you to describe the type of the parameters accepted by your method, as well as the type of the returned value, if any.

Now that this done, lets create a Window class which will instantiate our Foo class and pass it to JavaScript:

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

This PyQt-HTML masterpiece looks like this:

![Example](pyqt-webkit-tut2.png)

Clicking the "Compute" button doubles the value in the input widget, clicking Quit... quits the application.

In this example, we create `self.foo`, an instance of the Foo class, then expose it to our QWebView with the line:

    view.page().mainFrame().addToJavaScriptWindowObject("foo", self.foo)

We then feed our QWebView with some HTML code with `view.setHtml()`. Note how JavaScript code can now refer to our foo object as if it was a native JavaScript object.

(Complete code for this example is available as a <a href="https://gist.github.com/1647398">github gist</a>)

----

Console
Palette
Menu
Widgets
Setup
Icons
Live updates
