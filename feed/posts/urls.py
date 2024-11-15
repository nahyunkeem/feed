from django.urls import path
from .views import PostListView, PostListAPIView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("search", PostListAPIView.as_view()),
]