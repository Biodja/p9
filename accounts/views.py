from accounts.forms import CreationCompte
from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model

# Create your views here.

User = get_user_model()


def signup(request):
    if request.method == "POST":
        forms = CreationCompte(request.POST)
        if forms.is_valid():
            forms.save()

            return redirect("Home")
        else:
            print("Champs invalid")
            print(forms.errors)
            print(request.POST)

    else:
        forms = CreationCompte()

    return render(request, "accounts/signup.html", context={"forms": forms})


def afficher_flux(request):

    return render(request, "timeline.html", context={})


def login(request):

    return redirect("login")


def logout(request):

    return redirect("login")
