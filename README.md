# inkah-python

Python utilities for tracing distributed python services using [Inkah](https://github.com/inkah-trace)/

## Flask

Using some standard helper methods on the [Flask](http://flask.pocoo.org/) application object, inkah-python
provides a method to help instrument your Flask applications. This places an InkahSpan object on the Flask `g`
object that is scoped to each request so you can access the current span anywhere.

### Usage
```python
# Setup
from flask import Flask
from inkah.flask_utils import Trace

app = Flask(__name__)
trace = Trace(app)

# Accessing the current InkahSpan and creating an annotation
from flask import g

g.inkah_span.annotate('Hello, Inkah!')
```

Flask() method that automatically sets up tracing for each
request that Flask receives and provides a simple API to annotate the current
Inkah span.
