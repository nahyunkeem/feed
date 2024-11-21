from django.urls import path
from .views import PostListView, PostListAPIView, PostList, PostLike


urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("search", PostListAPIView.as_view()),
    path("filter", PostList.as_view()),
    path("likes/<int:pk>", PostLike.as_view(), name="post_likes"),
]
