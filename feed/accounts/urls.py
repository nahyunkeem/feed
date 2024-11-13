from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignUpAPIView.as_view()),
    path("signin/", views.SigninAPIView.as_view()),
]