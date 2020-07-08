from django_request_mapping import UrlPattern

from web.views import UserView, CourseView, HelloView

urlpatterns = UrlPattern()
# urlpatterns.register(BlogView)
urlpatterns.register(UserView)
urlpatterns.register(CourseView)
urlpatterns.register(HelloView)

