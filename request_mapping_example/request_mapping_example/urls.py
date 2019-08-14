from django.urls import path, include

urlpatterns = [
    path('api/v1/', include("blog.urls")),
]
