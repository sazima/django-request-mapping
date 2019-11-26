from django.http import JsonResponse, HttpResponse
from django.views import View

from django_request_mapping import request_mapping


@request_mapping("/blog")
class BlogView(View):
    @request_mapping(value="/hidden", method="get")
    def hidden(self, request, *args, **kwargs):
        # request.
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


@request_mapping("/user")
class UserView(View):
    @request_mapping("/info/")
    def get_user_info(self, request, *args, **kwargs):
        data = request.GET
        return JsonResponse(data)

    @request_mapping("/info/", method="post")
    def update(self, request):
        return JsonResponse({})


@request_mapping("/course")
class CourseView(View):
    @request_mapping("/")
    def get_list(self, request, *args, **kwargs):
        return HttpResponse("ok")

    @request_mapping("/<int:code>")
    def get_by_code(self, request, code):
        return JsonResponse({
            'code': code
        })
