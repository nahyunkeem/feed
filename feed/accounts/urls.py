from django.urls import path, include
from .views import SignUpAPIView, SigninAPIView

urlpatterns = [
    path("signup/", SignUpAPIView.as_view()),
    path("signin/", SigninAPIView.as_view()),
]