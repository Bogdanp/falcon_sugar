import gc
import falcon
import timeit

from falcon_sugar import Resource


class PeopleBaseline:
    def on_get(self, req, resp):
        resp.media = {}


class People(Resource):
    def on_get(self, req, resp):
        return {}


people_baseline = PeopleBaseline()
people = People()
req, resp = falcon.Request({
    "REQUEST_METHOD": "GET",
    "PATH_INFO": "/",
    "wsgi.input": "",
    "wsgi.errors": ""
}), falcon.Response()


def baseline():
    return people_baseline.on_get(req, resp)


def sugar():
    return people.on_get(req, resp)


print("baseline", timeit.timeit(baseline))
gc.collect()
print("sugar", timeit.timeit(sugar))
