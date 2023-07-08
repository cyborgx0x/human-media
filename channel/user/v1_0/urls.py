from django.urls import path

from channel.user.v1_0.views import ImportAPIView, SearchAPIView

urlpatterns = [
    path("", SearchAPIView.as_view(), name="search-channel"),
    path("import/", ImportAPIView.as_view, name="import-channel"),
]
