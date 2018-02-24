import falcon
import pytest

from falcon.testing import TestClient
from falcon_sugar import Resource


class People(Resource):
    def on_get(self, req, resp):
        return {"people": []}

    def on_post(self, req, resp):
        return falcon.HTTP_201, {}


class Person(Resource):
    def on_delete(self, req, resp, pk):
        return


@pytest.fixture
def app():
    app = falcon.API()
    app.add_route("/people", People())
    app.add_route("/people/{pk}", Person())
    return app


@pytest.fixture
def client(app):
    return TestClient(app)
