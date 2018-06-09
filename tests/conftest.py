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


class Butterflies(Resource):
    def on_post(self, req, resp):
        resp.status = falcon.HTTP_400
        resp.media = {}


@pytest.fixture
def app():
    app = falcon.API()
    app.add_route("/people", People())
    app.add_route("/people/{pk}", Person())
    app.add_route("/butterflies", Butterflies())
    return app


@pytest.fixture
def client(app):
    return TestClient(app)
