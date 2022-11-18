from django.urls import path, include

urlpatterns = [
    path("api/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
]
