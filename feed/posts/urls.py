from django.urls import path
from .views import PostListView, PostListAPIView, PostRetrieveAPIView

urlpatterns = [
    path("", PostListView.as_view(), name="post_list"),
    path("search", PostListAPIView.as_view()),
    path("<int:pk>", PostRetrieveAPIView.as_view(), name="post-detail"),
]