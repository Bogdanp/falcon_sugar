# falcon_sugar

[![Build Status](https://travis-ci.org/Bogdanp/falcon_sugar.svg?branch=master)](https://travis-ci.org/Bogdanp/falcon_sugar)
[![Maintainability](https://api.codeclimate.com/v1/badges/9ab06cb5a4ee924e0be4/maintainability)](https://codeclimate.com/github/Bogdanp/falcon_sugar/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/9ab06cb5a4ee924e0be4/test_coverage)](https://codeclimate.com/github/Bogdanp/falcon_sugar/test_coverage)

A little bit of sugar for [Falcon] apps.


## Installation

    pipenv install falcon_sugar

or

    pipenv install falcon_sugar[marshmallow]


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


### `falcon_sugar.marshmallow`

A [Marshmallow]-based validator.

``` python
from falcon_sugar import Resource, marshmallow
from marshmallow import Schema, fields, post_load, validate


class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True, validate=[validate.Range(0, 130)])

    @post_load
    def make_person(self, data):
        return PersonModel(**data)


class People(Resource):
    person_schema = PersonSchema()

    @marshmallow.dump(person_schema, many=True)
    def on_get(self, req, resp):
        return [PersonModel(id=1, name="Jim Gordon", age=36)]

    @marshmallow.validate(person_schema)
    @marshmallow.dump(person_schema)
    def on_post(self, req, resp):
        person = req.context["marshmallow"]
        person.save()
        return falcon.HTTP_201, person
```


## Limitations

Any decorator that doesn't return the result of the decorated function
will make it so that `Resource`s don't return a result.  This means
that builtin Falcon decorators like `before` and `after` are
incompatible with this library.


## License

falcon_sugar is licensed under Apache 2.0.  Please see
[LICENSE] for licensing details.


[Falcon]: https://falconframework.org
[Marshmallow]: https://marshmallow.readthedocs.io
[LICENSE]: https://github.com/Bogdanp/falcon_sugar/blob/master/LICENSE
