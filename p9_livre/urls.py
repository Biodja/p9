

"""p9 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    

    path('posts/', views.afficher_flux, name='posts'),
    path('Home/' , views.afficher_home,name="Home"),
    path('modale_ticket_reviews/' ,views.afficher_review,name="timeline5"),
    path('abonnement/' ,views.Subscriptions.as_view(),name="abonnement"),
    path('delete_abonnement/<followed_user_id>/' ,views.DeleteSubscription.as_view(),name="delete_subscription"),
    path('essai/', views.afficher_review),
    path('index/', views.afficher_review , name='index'),
    path('demande_de_critique/',views.publication_ticket,name="demande"),
    path('fenêtre_repondre/<ticket_id>/',views.repondre_ticket,name="reponse"),
]
