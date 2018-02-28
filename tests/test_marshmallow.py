import falcon
import pytest

from collections import namedtuple
from falcon.testing import TestClient
from falcon_sugar import Resource, marshmallow
from marshmallow import Schema, fields, post_load, validate


class PersonModel(namedtuple("PersonModel", ("name", "age"))):
    pass


class PersonSchema(Schema):
    name = fields.String(required=True)
    age = fields.Integer(required=True, validate=[validate.Range(0, 130)])

    @post_load
    def make_person(self, data):
        return PersonModel(**data)


class People(Resource):
    person_schema = PersonSchema()

    @marshmallow.validate(person_schema)
    def on_post(self, req, resp):
        person = req.context["marshmallow"]
        assert isinstance(person, PersonModel)
        return falcon.HTTP_201, self.person_schema.dump(person)


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


def test_marshmallow_populates_request_context_with_the_validation_result(client):
    # Given that I have an app client
    # When I make a valid request to create a person
    response = client.simulate_post("/people", json={
        "name": "Jim Gordon",
        "age": 36,
    })

    # Then I should get back a 200 response
    assert response.status_code == 201
