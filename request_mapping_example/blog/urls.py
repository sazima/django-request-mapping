from django_request_mapping import UrlPattern

from blog.views import UserView, CourseView

urlpatterns = UrlPattern()
# urlpatterns.register(BlogView)
urlpatterns.register(UserView)
urlpatterns.register(CourseView)

