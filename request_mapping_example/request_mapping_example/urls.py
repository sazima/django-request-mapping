from django.urls import path, include

import django_request_mapping
from blog.views import *

urlpatterns = [
    path('api/v1/', include(django_request_mapping.urls)),
]
