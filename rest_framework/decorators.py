"""
The most imporant decorator in this module is `@api_view`, which is used
for writing function-based views with REST framework.

There are also various decorators for setting the API policies on function
based views, as well as the `@action` and `@link` decorators, which are
used to annotate methods on viewsets that should be included by routers.
"""
from __future__ import unicode_literals
from rest_framework.compat import six
from rest_framework.views import APIView
import types


def api_view(http_method_names):

    """
    Decorator that converts a function-based view into an APIView subclass.
    Takes a list of allowed methods for the view as an argument.
    """

    def decorator(func):

        WrappedAPIView = type(
            six.PY3 and 'WrappedAPIView' or b'WrappedAPIView',
            (APIView,),
            {'__doc__': func.__doc__}
        )

        # Note, the above allows us to set the docstring.
        # It is the equivalent of:
        #
        #     class WrappedAPIView(APIView):
        #         pass
        #     WrappedAPIView.__doc__ = func.doc    <--- Not possible to do this

        # api_view applied without (method_names)
        assert not(isinstance(http_method_names, types.FunctionType)), \
            '@api_view missing list of allowed HTTP methods'

        # api_view applied with eg. string instead of list of strings
        assert isinstance(http_method_names, (list, tuple)), \
            '@api_view expected a list of strings, recieved %s' % type(http_method_names).__name__

        allowed_methods = set(http_method_names) | set(('options',))
        WrappedAPIView.http_method_names = [method.lower() for method in allowed_methods]

        def handler(self, *args, **kwargs):
            return func(*args, **kwargs)

        for method in http_method_names:
            setattr(WrappedAPIView, method.lower(), handler)

        WrappedAPIView.__name__ = func.__name__

        WrappedAPIView.renderer_classes = getattr(func, 'renderer_classes',
                                                  APIView.renderer_classes)

        WrappedAPIView.parser_classes = getattr(func, 'parser_classes',
                                                APIView.parser_classes)

        WrappedAPIView.authentication_classes = getattr(func, 'authentication_classes',
                                                        APIView.authentication_classes)

        WrappedAPIView.throttle_classes = getattr(func, 'throttle_classes',
                                                  APIView.throttle_classes)

        WrappedAPIView.permission_classes = getattr(func, 'permission_classes',
                                                    APIView.permission_classes)

        return WrappedAPIView.as_view()
    return decorator


def renderer_classes(renderer_classes):
    def decorator(func):
        func.renderer_classes = renderer_classes
        return func
    return decorator


def parser_classes(parser_classes):
    def decorator(func):
        func.parser_classes = parser_classes
        return func
    return decorator


def authentication_classes(authentication_classes):
    def decorator(func):
        func.authentication_classes = authentication_classes
        return func
    return decorator


def throttle_classes(throttle_classes):
    def decorator(func):
        func.throttle_classes = throttle_classes
        return func
    return decorator


def permission_classes(permission_classes):
    def decorator(func):
        func.permission_classes = permission_classes
        return func
    return decorator


def link(**kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for GET requests.
    """
    def decorator(func):
        func.bind_to_method = 'get'
        func.kwargs = kwargs
        return func
    return decorator


def action(**kwargs):
    """
    Used to mark a method on a ViewSet that should be routed for POST requests.
    """
    def decorator(func):
        func.bind_to_method = 'post'
        func.kwargs = kwargs
        return func
    return decorator