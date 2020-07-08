"""
@author: sazima
@time: 2019/8/9 下午20:03
@desc:
"""
import inspect
import logging
from functools import update_wrapper, partial

from django.utils.decorators import classonlymethod
from django.views import View
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger('request_mapping.decorator')


def request_mapping(value: str, method: str = 'get', path_type: str = 'path'):
    """
    :param value: The path mapping URIs (e.g. "/myPath.do")
    :param method:  The HTTP request methods to map to, narrowing the primary mapping:
     get, post, head, options, put, patch, delete, trace
    :param path_type: path or re_path
    """

    # todo: type annotation error
    def get_func(o: type(View), v: str):
        setattr(o, 'request_mapping', RequestMapping(v, method, path_type))
        if inspect.isclass(o):
            if not value.startswith('/'):
                logger.warning("values should startswith / ")
            o.as_django_request_mapping_view = as_django_request_mapping_view
            o.django_request_mapping_dispatch = django_request_mapping_dispatch
        return o

    return partial(get_func, v=value)


@classonlymethod
def as_django_request_mapping_view(cls, actions=None, **initkwargs):
    """
    Because of the way class based views create a closure around the
    instantiated view, we need to totally reimplement `.as_view`,
    and slightly modify the view function that is created and returned.
    """
    # The name and description initkwargs may be explicitly overridden for
    # certain route confiugurations. eg, names of extra actions.
    cls.name = None
    cls.description = None

    # The suffix initkwarg is reserved for displaying the viewset type.
    # This initkwarg should have no effect if the name is provided.
    # eg. 'List' or 'Instance'.
    cls.suffix = None

    # The detail initkwarg is reserved for introspecting the viewset type.
    cls.detail = None

    # Setting a basename allows a view to reverse its action urls. This
    # value is provided by the router through the initkwargs.
    cls.basename = None

    # actions must not be empty
    if not actions:
        raise TypeError("The `actions` argument must be provided when "
                        "calling `.as_view()` on a ViewSet. For example "
                        "`.as_view({'get': 'list'})`")

    # sanitize keyword arguments
    for key in initkwargs:
        if key in cls.http_method_names:
            raise TypeError("You tried to pass in the %s method name as a "
                            "keyword argument to %s(). Don't do that."
                            % (key, cls.__name__))
        if not hasattr(cls, key):
            raise TypeError("%s() received an invalid keyword %r" % (
                cls.__name__, key))

    # name and suffix are mutually exclusive
    if 'name' in initkwargs and 'suffix' in initkwargs:
        raise TypeError("%s() received both `name` and `suffix`, which are "
                        "mutually exclusive arguments." % (cls.__name__))

    def view(request, *args, **kwargs):
        self = cls(**initkwargs)
        # We also store the mapping of request methods to actions,
        # so that we can later set the action attribute.
        # eg. `self.action = 'list'` on an incoming GET request.
        self.action_map = actions

        # Bind methods to actions
        # This is the bit that's different to a standard view
        for method, action in actions.items():
            handler = getattr(self, action)
            setattr(self, '_request_mapping_%s_' % method, handler)

        self.request = request
        self.args = args
        self.kwargs = kwargs

        # And continue as usual
        return self.django_request_mapping_dispatch(request, *args, **kwargs)

    # take name and docstring from class
    update_wrapper(view, cls, updated=())

    # and possible attributes set by decorators
    # like csrf_exempt from django_request_mapping_dispatch
    update_wrapper(view, cls.django_request_mapping_dispatch, assigned=())

    # We need to set these on the view function, so that breadcrumb
    # generation can pick out these bits of information from a
    # resolved URL.
    view.cls = cls
    view.initkwargs = initkwargs
    view.actions = actions
    return csrf_exempt(view)


def django_request_mapping_dispatch(self, request, *args, **kwargs):
    # much same as Django's dispatch
    self.request = request
    if request.method.lower() in self.http_method_names:
        handler = getattr(self, '_request_mapping_%s_' % request.method.lower(), self.http_method_not_allowed)
    else:
        handler = self.http_method_not_allowed
    # fix: AttributeError: 'WSGIRequest' object has no attribute 'data' while using rest-framework
    initialize_request = getattr(self, 'initialize_request', None)
    if initialize_request:
        request = initialize_request(request, *args, **kwargs)
    return handler(request, *args, **kwargs)


class RequestMapping:
    def __init__(self, value: str, method: str, path_type: str):
        self.value: str = value
        self.method: str = method
        self.path_type = path_type
