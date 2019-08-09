make urlpatterns very easy to use.

### Example

```python
from django_request_mapping import request_mapping


@request_mapping(value="/user")
class UserView(View):

    @request_mapping(value="/get_info/")
    def get_user_info_by_token(self, request, *args, **kwargs):
        return HttpResponse("ok")

    @request_mapping(value="/get_list/<int:year>/")
    def some_others(self, request, year, *args, **kwargs):
        return HttpResponse("ok")
        
    @request_mapping(value="/login/", method="post")
    def login(self, request, *args, **kwargs):
        return HttpResponse("ok")

```

```bash
python manage.py runserver
```

and request url is :

post:  http://localhost:8000/user/login/

get:  http://localhost:8000/user/get_info/

get: http://localhost:8000/user/get_list/1999/
