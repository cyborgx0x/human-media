from django.urls import path

from . import views

app_name = "channel"
urlpatterns = [
    path("<str:keyword>", views.search, name="search"),
    path("import/", views.import_file, name="import"),
]
