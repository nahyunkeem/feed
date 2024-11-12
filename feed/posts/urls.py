from django.urls import path
from . import views

urlpatterns = [
    path("", views.PostListAPIView.as_view()),
]