from django.http import JsonResponse, HttpResponse
from django.views import View

from django_request_mapping import request_mapping


@request_mapping("/user")
class UserView(View):
    @request_mapping("/info/")
    def get_user_info(self, request, *args, **kwargs):
        data = request.GET
        return JsonResponse(data)

    @request_mapping("/info/", method="post")
    def update(self, request):
        return JsonResponse({
            'msg': 'ok'
        })

    @request_mapping(r'/(?P<pk>\w{5})/$', path_type='re_path', method='post')
    def test(self, request, pk):
        return JsonResponse({
            "pk": pk
        })


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
