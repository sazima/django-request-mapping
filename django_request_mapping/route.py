"""
@author: sazima
@time: 2019/8/14 下午21:00
@desc:
"""
from typing import Dict, Iterable, Any

from django.urls import path

from .decorator import RequestMapping


class Urls(object):
    def __init__(self, urlpatterns: list):
        self.urlpatterns = urlpatterns


class UrlPattern(list):
    urlpatterns = list()
    class_paths = list()

    def register(self, clazz):
        class_request_mapping: RequestMapping = getattr(clazz, 'request_mapping', None)
        assert class_request_mapping is not None, 'view class should use request_mapping decorator.'
        # path value on class decorator
        class_path = class_request_mapping.path
        if class_path and class_path in self.class_paths:
            raise RuntimeError('duplicated request_mapping value')

        url_patterns_dict: Dict[str, Dict] = dict()

        for func_name in dir(clazz):
            func = getattr(clazz, func_name)
            mapping: RequestMapping = getattr(func, 'request_mapping', None)
            if mapping is None:
                continue
            request_method = mapping.method
            # path value on method decorator
            method_path = mapping.path
            full_path = class_path + method_path
            if full_path in url_patterns_dict:
                temp_func_name = url_patterns_dict[full_path].setdefault(request_method, func_name)
                # check if method and path are duplicated
                assert temp_func_name == func_name, "path: {} with method: {} is duplicated".format(
                    full_path,
                    request_method
                )
            else:
                url_patterns_dict[full_path] = {request_method: func_name}

        self.update_urlpatterns(clazz, url_patterns_dict)

    def update_urlpatterns(self, clazz, url_patterns_dict):
        self.urlpatterns.extend([
            path(
                self._get_full_path(full_path),
                clazz.as_view(action)) for full_path, action in url_patterns_dict.items()
        ])

    def __iter__(self, *args, **kwargs):
        for item in self.urlpatterns:
            yield item

    @staticmethod
    def _get_full_path(full_path: str) -> str:
        # Remove redundant slants
        full_path = full_path.replace('//', '/', 1)
        if full_path.startswith('/'):
            return full_path[1:]
        return full_path

    @property
    def urls(self) -> Urls:
        """
        make to support:
            pattern = UrlPattern()
            pattern.register(UserView)
            urlpatterns = [path(r'', include(pattern.urls)]
        """
        return Urls(self.urlpatterns)

    def append(self, value: Any):
        return self.urlpatterns.append(value)

    def extend(self, iterable: Iterable[Any]):
        return self.urlpatterns.extend(iterable)

    def reverse(self):
        return self.urlpatterns.reverse()
