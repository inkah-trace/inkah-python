# inkah-python

Python utilities for tracing distributed python services using [Inkah](https://github.com/mleonard87/inkah)/

## Flask

Using some standard helper methods on the [Flask](http://flask.pocoo.org/) application object inkah-python
provides a familiar Flask() method that automatically sets up tracing for each
request that Flask receives and provides a simple API to annotate the current
Inkah span.


## requests

The
