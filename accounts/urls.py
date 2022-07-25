
from django.urls import path, include

from accounts.views import afficher_flux, signup , login



urlpatterns = [
    path('', login,  name='timeline'),
    path('', include("django.contrib.auth.urls")),
    path('signup/', signup, name="signup"),
    path('accounts/', signup, name="accounts"),



] 