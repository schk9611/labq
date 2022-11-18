from django.urls import path
from api.views import SeoulOpenDataVeiw

urlpatterns = [
    path("seoul/drainpipe-rainfall/", SeoulOpenDataVeiw.as_view()),
]
