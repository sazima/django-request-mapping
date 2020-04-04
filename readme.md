make urlpatterns very easy to use.

#### Requirements

```bash
django == 2.x
```

#### Install

Install and update using pip:


```python
pip install -U  django-request-mapping
```


#### A Simple Example


view.py

```python
from django_request_mapping import request_mapping


@request_mapping("/user")
class UserView(View):

    @request_mapping("/login/", method="post")
    def login(self, request, *args, **kwargs):
        return HttpResponse("ok")

    @request_mapping("/signup/", method="post")
    def register(self, request, *args, **kwargs):
        return HttpResponse("ok")
    
    @request_mapping("/<int:user_id>/role/")
    def get_role(self, request, user_id):
       return HttpResponse("ok") 
    
    @request_mapping("/<int:pk/", method='delete')
    def delete(self, request, pk):
        User.objects.filter(pk=pk).delete()
        return HttpResponse("ok")
    

@request_mapping("/role")
class RoleView(View):
    # ...

```


urls.py
```python
from django_request_mapping import UrlPattern
urlpatterns = UrlPattern()
urlpatterns.register(UserView)
urlpatterns.register(RoleView)
```

and request urls are:

```bash
post:  http://localhost:8000/user/login/
post:  http://localhost:8000/user/signup/
get:  http://localhost:8000/user/1/role/
delete: http://localhost:8000/user/1/
# ...
```


#### Full Example

https://github.com/sazima/django-request-mapping/tree/master/example

