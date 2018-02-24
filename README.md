# falcon_sugar

[![Build Status](https://travis-ci.org/Bogdanp/falcon_sugar.svg?branch=master)](https://travis-ci.org/Bogdanp/falcon_sugar)
[![Maintainability](https://api.codeclimate.com/v1/badges/9ab06cb5a4ee924e0be4/maintainability)](https://codeclimate.com/github/Bogdanp/falcon_sugar/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9ab06cb5a4ee924e0be4/test_coverage)](https://codeclimate.com/github/Bogdanp/falcon_sugar/test_coverage)

A little bit of sugar for [Falcon] apps.


## Installation

    pipenv install falcon_sugar


## Usage

### `falcon_sugar.Resource`

This class lets you write request handlers that `return` their results
rather than writing to `resp.media`:

``` python
import falcon

from falcon_sugar import Resource


# This:
class People(Resource):
  def on_get(self, req, resp):
    return {"people": []}

  def on_post(self, req, resp):
    return falcon.HTTP_201, {}


class Person(Resource):
  def on_delete(self, req, resp, pk):
    pass


# Instead of this:
class People:
  def on_get(self, req, resp):
    resp.media = {"people": []}

  def on_post(self, req, resp):
    resp.status = falcon.HTTP_201
    resp.media = {}


class Person(Resource):
  def on_delete(self, req, resp, pk):
    resp.status = falcon.HTTP_201
```


## License

falcon_sugar is licensed under Apache 2.0.  Please see
[LICENSE] for licensing details.


[Falcon]: https://falconframework.org
[LICENSE]: https://github.com/Bogdanp/falcon_sugar/blob/master/LICENSE
