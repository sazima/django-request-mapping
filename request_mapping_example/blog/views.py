from django.http import JsonResponse

# Create your views here.
from django.views import View

from django_request_mapping import request_mapping


@request_mapping("/blog")
class BlogView(View):
    @request_mapping(value="/hidden", method="get")
    def hidden(self, request, *args, **kwargs):
        return JsonResponse({
            "msg": "ok"
        })

    @request_mapping(value="/hidden", method="post")
    def hidden2(self, request, *args, **kwargs):
        return JsonResponse({
            "msg": "ok"
        })

    @request_mapping(value="/delete", method="post")
    def delete(self, request, *args, **kwargs):
        return JsonResponse({
            "msg": "ok"
        })
