# PyQt+WebKit experiments part 2: debugging

----

(This is part 2 of the [PyQt+WebKit experiments series](/article-series/pyqtwebkit-experiments/))

In [Part 1](/2012/01/20/swimming-against-the-stream-or-preparing-for-next-stream-change-pyqtwebkit-experiments/) I described how to embed WebKit in a PyQt application and how to expose PyQt objects in WebKit and manipulate them with JavaScript.

Even if you are a great JavaScript master, you can't avoid the occasional typo while writing JavaScript code in your application. This can be quite frustrating with QtWebKit because it likes to stay quiet: it won't tell you about any error.

Let's have a look at an example.

First here is loader.py, a simple Python script which loads a block of HTML:

    ${loader.py}

And here is "broken.html", our broken HTML code:

    ${broken.html}

Notice the missing 't' in "resul /= 4"?

The last-resort, grandpa-debugged-js-this-way, debugging tool is still there: the mighty alert() function. Just stuff your code with calls to alert() and be happy... Anyone ever wrote code like that?

    ${broken-alert.html}

Easy enough, no? With the great alert() function we can quickly pinpoint the bug in our brokenFunction() is between alert("2") and alert("3").

## Can we do better?

alert()-style debugging gets old very fast. Clicking that "OK" button is a pain. Fortunately, there is a way to get more useful feedback from our PyQt application.

The job of the QWebView class is to show the content of a QWebPage instance. By default QWebView creates its own instance of QWebPage, but it is possible to replace this instance with our own QWebPage. The QWebPage class has a few virtual methods. Among them, the javaScriptConsoleMessage() method is the one we are looking for: it is called every time console.log() is called from JavaScript.

Here is an implementation of WebPage which uses Python logging module to get JavaScript console messages out:

    ${webpage.py}

And here is "loader-log.py", a loader which uses this class:

    ${loader-log.py}

If we load "broken.html" with "loader-log.py" we get the following on stderr:

    $ python loader-log.py broken.html
    WARNING:root:JsConsole(undefined:0): ReferenceError: Can't find variable: resul

That should make it easier to find and fix our bug, even if we don't get very useful file names or line numbers.

javaScriptConsoleMessage() receives all console messages. This means our logger will also print out calls to console.log(). Here is "console-log.html":

    ${console-log.html}

When loaded with "loader-log.py", we get this output:

    $ python loader-log.py console-log.html
    WARNING:root:JsConsole(about:blank:5): result: 4
    WARNING:root:JsConsole(about:blank:5): result: 7
    WARNING:root:JsConsole(about:blank:5): result: 1.75

## Not good enough?

Getting the output of console.log() is nice, but modern browsers have much more efficient tools: if you open "broken.html" with Rekonq and look at the output in the Web Inspector Console, you can not only see console output, but you can also easily inspect your HTML tree and many other things.

![Rekonq Web Inspector](rekonq-webinspector.png)

Like us, Rekonq uses QtWebKit, so is there a way to get a similar tool?

It is actually possible. Rekonq uses a class named QWebInspector. All that is necessary to get a nice inspector tool for our application is to:

1. Get the QWebView page
1. set the QWebSettings.DeveloperExtrasEnabled attribute on this page
1. Instantiate a QWebInspector
1. Pass the view page to the inspector

Here is "loader-webinspector.py", a new HTML loader which can show a web inspector when one presses F12:

    ${loader-webinspector.py}

The four steps I described are done in the "setupInspector()" method.

And here is "console-webinspector.html":

    ${console-webinspector.html}

It is similar to "console-log.html" but takes advantage of two new features which do not work with the previous approach:

- printf-style formatting: that is, printing the value of `result` with `"result: %d", result`, not `"result: " + result`
- log categorization: you can use console.warn() and console.error() to get different type of output. These methods worked with the previous approach, but the categorization was lost.

Loading "console-webinspector.html" with "loader-webinspector.py" and pressing F12 we get this:

![Loader with web inspector](loader-webinspector.png)

## Closing words

These two approaches should help you track down the nastiest bugs in your embedded JavaScript code. The Web Inspector approach is probably the most powerful one, but the Python logging approach can also be useful when tracking down bugs where it is more practical to have one single log output for both the PyQt and the JavaScript sides.
