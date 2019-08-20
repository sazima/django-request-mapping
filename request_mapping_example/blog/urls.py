from blog.views import BlogView, UserView
from django_request_mapping import UrlPattern

urlpatterns = UrlPattern()
urlpatterns.register(BlogView)
urlpatterns.register(UserView)

