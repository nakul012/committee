from .views import (
    UserLoginView,
    UserLogoutView,UserSignUpView
)
from django.urls import path


urlpatterns = [
    path("v1/signup/", UserSignUpView.as_view()),
    path("v1/login/", UserLoginView.as_view()),
    path("v1/logout/", UserLogoutView.as_view()),
]
