"""
@author: sazima
@time: 2019/8/14 下午21:00
@desc:
"""
from typing import Dict

from django.urls import path


class Urls(object):
    def __init__(self, urlpatterns: list):
        self.urlpatterns = urlpatterns


class UrlPattern(list):
    urlpatterns = list()
    prefix_paths = list()

    def register(self, clazz):
        clazz = self._get_true_class(clazz)
        prefix_path = getattr(clazz, 'request_mapping', {}).get('value', '')

        if prefix_path and prefix_path in self.prefix_paths:
            raise RuntimeError('duplicated request_mapping value')
        url_patterns_dict: Dict[str, Dict] = dict()
        for func_name in dir(clazz):
            func = getattr(clazz, func_name)
            mapping = getattr(func, 'request_mapping', None)
            if not mapping:
                continue
            request_method = mapping.get('method')
            request_path = mapping.get('value')
            full_path = prefix_path + request_path
            try:
                temp_func_name = url_patterns_dict[full_path].setdefault(request_method, func_name)
                assert temp_func_name == func_name, "path: {} with method: {} is duplicated".format(
                    full_path,
                    request_method
                )
            except KeyError:
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
        if full_path.startswith('/'):
            return full_path[1:]
        return full_path

    @staticmethod
    def _get_true_class(clazz):
        if hasattr(clazz, '__wrapped__'):
            clazz = getattr(clazz, '__wrapped__')
        return clazz

    @property
    def urls(self) -> Urls:
        return Urls(self.urlpatterns)
