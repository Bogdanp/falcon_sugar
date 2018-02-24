import falcon
import functools

HANDLER_METHOD_NAMES = {
    "on_delete",
    "on_get",
    "on_options",
    "on_patch",
    "on_post",
    "on_put",
}


def handler(method):
    @functools.wraps(method)
    def wrapper(self, req, resp, *args, **kwargs):
        response_data = method(self, req, resp, *args, **kwargs)
        if isinstance(response_data, tuple):
            resp.status, resp.media = response_data

        elif response_data is None:
            resp.status = falcon.HTTP_204

        else:
            resp.media = response_data

    return wrapper


class resource(type):
    def __new__(cls, name, bases, namespace):
        for name, value in namespace.items():
            if name in HANDLER_METHOD_NAMES:
                namespace[name] = handler(value)

        return super().__new__(cls, name, bases, namespace)


class Resource(metaclass=resource):
    """Makes it possible for resource handlers to write to
    ``resp.media`` by returning.

    Example:
      >>> class People(Resource):
      ...   def on_get(self, req, resp):
      ...     return {"people": []}
      ...
      ...   def on_post(self, req, resp):
      ...     return falcon.HTTP_201, {}
    """
