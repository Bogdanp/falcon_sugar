import falcon
import pytest

from collections import namedtuple
from falcon.testing import TestClient
from falcon_sugar import Resource, marshmallow
from marshmallow import Schema, fields, post_dump, post_load, validate


class PersonModel(namedtuple("PersonModel", ("id", "name", "age", "secret"))):
    pass


class PersonSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    age = fields.Integer(required=True, validate=[validate.Range(0, 130)])

    @post_dump(pass_many=True)
    def prepare_dump(self, data, many):
        if many:
            return {"people": data}
        return data

    @post_load
    def make_person(self, data):
        return PersonModel(id=1, secret="verysecret", **data)


class People(Resource):
    person_schema = PersonSchema()

    @marshmallow.dump(person_schema, many=True)
    def on_get(self, req, resp):
        return [
            PersonModel(id=1, secret="sosecret!", name="Jim Gordon", age=36),
            PersonModel(id=2, secret="othersec!", name="Bruce Wayne", age=30),
        ]

    @marshmallow.validate(person_schema)
    @marshmallow.dump(person_schema)
    def on_post(self, req, resp):
        person = req.context["marshmallow"]
        assert isinstance(person, PersonModel)
        return falcon.HTTP_201, person


@pytest.fixture
def app():
    app = falcon.API()
    app.add_route("/people", People())
    return app


@pytest.fixture
def client(app):
    return TestClient(app)


def test_marshmallow_validates_requests(client):
    # Given that I have an app client
    # When I make an invalid request to create a person
    response = client.simulate_post("/people", json={
        "test": 1,
    })

    # Then I should get back a 400 response
    assert response.status_code == 400

    # And the response should contain a description of the issues
    assert response.json == {
        "message": "request failed validation",
        "fields": ["age", "name"],
        "errors": {
            "age": ["Missing data for required field."],
            "name": ["Missing data for required field."],
        }
    }


def test_marshmallow_dumps_responses(client):
    # Given that I have an app client
    # When I make a request to get a list of people
    response = client.simulate_get("/people")

    # Then I should get back a 200 response
    assert response.status_code == 200

    # And a valid response
    assert response.json == {
        "people": [
            {"id": 1, "name": "Jim Gordon", "age": 36},
            {"id": 2, "name": "Bruce Wayne", "age": 30},
        ],
    }


def test_marshmallow_validates_requests_and_dumps_responses(client):
    # Given that I have an app client
    # When I make a valid request to create a person
    response = client.simulate_post("/people", json={
        "name": "Jim Gordon",
        "age": 36,
    })

    # Then I should get back a 201 response
    assert response.status_code == 201

    # And a valid response
    assert response.json == {"id": 1, "name": "Jim Gordon", "age": 36}
