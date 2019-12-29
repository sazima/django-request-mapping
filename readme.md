make urlpatterns very easy to use.

#### Requirements
```bash
django == 2.x
```

#### Install

```python

pip install django-request-mapping

```


#### QuickStart

- view.py
```python
from django_request_mapping import request_mapping


@request_mapping("/user")
class UserView(View):

    @request_mapping("/get_info/")
    def get_user_info_by_token(self, request, *args, **kwargs):
        return HttpResponse("ok")

    @request_mapping(value="/get_list/<int:year>/")
    def some_others(self, request, year, *args, **kwargs):
        return HttpResponse("ok")
        
    @request_mapping("/login/", method="post")
    def login(self, request, *args, **kwargs):
        return HttpResponse("ok")

```

- urls.py

```python

from django_request_mapping import UrlPattern
urlpatterns = UrlPattern()
urlpatterns.register(UserView)

```

run

```bash
python manage.py runserver
```

and request urls are:


```bash
get:  http://localhost:8000/user/get_info/
get: http://localhost:8000/user/get_list/1999/
post:  http://localhost:8000/user/login/
```


#### Full Example

https://github.com/sazima/django-request-mapping/tree/master/request_mapping_example

