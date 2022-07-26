from django.urls import path, include

from accounts.views import logout, signup, login

urlpatterns = [
    path("", login, name="timeline"),

    path("", include("django.contrib.auth.urls")),
    path("signup/", signup, name="signup"),
]
