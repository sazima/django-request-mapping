from blog.views import BlogView
from django_request_mapping import UrlPattern

urlpatterns = UrlPattern()
urlpatterns.register(BlogView)
