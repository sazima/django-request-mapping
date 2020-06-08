"""
@author: sazima
@time: 2019/8/14 下午21:00
@desc:
"""
from typing import Dict, Iterable, Any, List, Tuple, Union

from django.urls import path, re_path

from .decorator import RequestMapping


class Urls(object):
    def __init__(self, urlpatterns):
        self.urlpatterns = urlpatterns


class UrlPattern(list):
    def __init__(self):
        self.urlpatterns: List[Union[path, re_path]] = list()

    def register(self, clazz):
        class_request_mapping: RequestMapping = getattr(clazz, 'request_mapping', None)
        if class_request_mapping is None:
            raise RuntimeError('view class should use request_mapping decorator.')

        # path value on class decorator
        class_path_value = class_request_mapping.value

        url_patterns_dict: Dict[Tuple[str, str], Dict] = dict()
        for func_name in dir(clazz):
            func = getattr(clazz, func_name)
            mapping: RequestMapping = getattr(func, 'request_mapping', None)
            if mapping is None:
                continue
            request_method = mapping.method
            # path value on method decorator
            method_path_value = mapping.value
            path_type = mapping.path_type
            full_value = class_path_value + method_path_value
            full_value = self._fix_path_value(full_value, path_type)

            if (path_type, full_value) in url_patterns_dict:
                temp_func_name = url_patterns_dict[(path_type, full_value)].setdefault(request_method, func_name)
                # check if method and path are duplicated
                assert temp_func_name == func_name, "path: {} with method: {} is duplicated".format(
                    full_value,
                    request_method
                )
            else:
                url_patterns_dict[(path_type, full_value)] = {request_method: func_name}

        self.update_urlpatterns(clazz, url_patterns_dict)

    def update_urlpatterns(self, clazz, url_patterns_dict):
        for (path_type, full_value), action in url_patterns_dict.items():
            if path_type == 'path':
                self.urlpatterns.append(
                    path(full_value, clazz.as_django_request_mapping_view(action))
                )
            elif path_type == 're_path':
                self.urlpatterns.append(
                    re_path(full_value, clazz.as_django_request_mapping_view(action))
                )
            else:
                raise RuntimeError('not a valid path_type')

    def __iter__(self, *args, **kwargs):
        for item in self.urlpatterns:
            yield item

    @staticmethod
    def _fix_path_value(full_value: str, path_type: str) -> str:
        # Remove redundant slants
        full_value = full_value.replace('//', '/', 1)
        if full_value.startswith('/'):
            full_value = full_value[1:]
        if path_type == 're_path':
            full_value = '^' + full_value
        return full_value

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
