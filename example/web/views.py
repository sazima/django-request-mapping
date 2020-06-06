from django.http import JsonResponse, HttpResponse
from django.views import View

from django_request_mapping import request_mapping


@request_mapping("/user")
class UserView(View):
    @request_mapping("/info/")
    def get_info(self, request):
        data = request.GET
        self.get()  # test
        return JsonResponse(data)

    @request_mapping("/info/", method="post")
    def update(self, request):
        return JsonResponse({
            'msg': 'ok'
        })

    @request_mapping("/delete_by_department/", method='delete')
    def delete_by_department(self, request):
        department_id = request.GET.get('department_id')
        # delete
        return JsonResponse({})

    @request_mapping("/group_by_<str:field_name>/")
    def group(self, request, field_name):
        # User.objects.values(field_name).annotate(count=Count('id')).order_by('id').all()
        return JsonResponse({'field_name': field_name})

    @request_mapping(r'/(?P<pk>\w{5})/$', path_type='re_path', method='post')
    def test(self, request, pk):
        return JsonResponse({
            "pk": pk
        })

    # It doesn't support the following code. You must use a decorator
    def get(self):
        print('this test test')
        return 'ok>>>>>>>>>>>>>>>>>>>>>>>>>>.'

    # It doesn't support the following code. You must use a decorator
    def delete(self):
        print('this test test')
        return "ok>>>>>>>>>>>>>>"


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
