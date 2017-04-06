# inkah-python

Python utilities for tracing distributed python services using [Inkah](https://github.com/inkah-trace)/

### Usage
```python
# Setup
from flask import Flask
from inkah.flask import Inkah

app = Flask(__name__)
trace = Inkah(app)

# Accessing the current InkahSpan and creating an annotation
from flask import g

g.inkah_span.annotate('Hello, Inkah!')
```
