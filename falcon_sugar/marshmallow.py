import falcon
import functools

try:
    import marshmallow

    HAS_MARSHMALLOW = True
except ImportError:  # pragma: no cover
    HAS_MARSHMALLOW = False


def dump(schema, **options):
    """Decorator for dumping response values using Marshmallow.

    Parameters:
      schema(marshmallow.Schema)
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, req, resp, *args, **kwargs):
            response = method(self, req, resp, *args, **kwargs)
            if isinstance(response, tuple):
                status, response = response
                return status, schema.dump(response, **options)
            return schema.dump(response, **options)
        return wrapper
    return decorator


def validate(schema):
    """Decorator for validating ``req.media`` using Marshmallow.

    Parameters:
      schema(marshmallow.Schema)
    """
    def decorator(method):
        @functools.wraps(method)
        def wrapper(self, req, resp, *args, **kwargs):
            try:
                req.context["marshmallow"] = schema.load(req.media)
                return method(self, req, resp, *args, **kwargs)
            except marshmallow.ValidationError as e:
                return falcon.HTTP_400, {
                    "message": "request failed validation",
                    "fields": sorted([f.name for f in e.fields]),
                    "errors": e.messages,
                }
        return wrapper
    return decorator


if not HAS_MARSHMALLOW:  # pragma: no cover
    def dump(schema):
        raise RuntimeError("marshmallow is not installed.  Run `pipenv install marshmallow`.")

    validate = dump
