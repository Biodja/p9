from itertools import chain
from .formulaires import (
    DemandeDeCritiquePublication,
    ReviewForm,
    UserFollowForm,
)
from .models import Ticket, Review, UserFollows
from django.db.models import CharField, Value
from django.shortcuts import render, redirect
from django.views import View
from django.utils.decorators import method_decorator
from urllib.parse import urlencode
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

_MESSAGES = {
    "unknown_user": "Utilisateur inconnu !",
    "do_not_follow_yourself": "Veuillez renseigner un nom d'utilisateur autre que le votre.",
    "subscription_succes": "Vous suivez désormais l'utilisateur {username} !",
    "already_following": "Vous suivez déjà l'utilisateur {username} !",
    "stopped_subscription": "Vous ne suivez désormais plus l'utilisateur {username}",
}


def afficher_review(request):
    # in views.py
    reviews = Review.objects.filter(user=request.user.id).all()
    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = Ticket.objects.filter(user=request.user.id).all()
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(
        request,
        "Home.html",
        context={"posts": posts, "publication": DemandeDeCritiquePublication()},
    )


# in feed.html
# Use the 'include' tag to reuse ticket and review elements between pages

...


@login_required
def afficher_flux(request):
    mes_tickets = Ticket.objects.filter(user=request.user.id).all()
    mes_critiques = Review.objects.filter(user=request.user.id).all()

    return render(
        request,
        "posts.html",
        context={"tickets": mes_tickets, "reviews": mes_critiques},
    )


@login_required
def afficher_home(request):
    reviews = Review.objects.filter(user=request.user.id).all()
    for user_follow in UserFollows.objects.filter(user=request.user.id):

        reviews |= Review.objects.filter(user=user_follow.followed_user)

    # returns queryset of reviews
    reviews = reviews.annotate(content_type=Value("REVIEW", CharField()))

    tickets = Ticket.objects.filter(user=request.user.id).all()
    for user_follow in UserFollows.objects.filter(user=request.user.id):

        tickets |= Ticket.objects.filter(user=user_follow.followed_user)
    # returns queryset of tickets
    tickets = tickets.annotate(content_type=Value("TICKET", CharField()))

    # combine and sort the two types of posts
    posts = sorted(
        chain(reviews, tickets), key=lambda post: post.time_created, reverse=True
    )
    return render(
        request,
        "Home.html",
        context={"posts": posts, "publication": DemandeDeCritiquePublication()},
    )


@login_required
def publication_ticket(request):

    if request.method == "POST":

        publication = DemandeDeCritiquePublication(request.POST, request.FILES)
        if [publication.is_valid()]:
            ticket = publication.save(commit=False)
            ticket.user = request.user
            ticket.save()

            return redirect("Home")
        else:
            print(publication.errors)
            print(request.POST)
    else:
        publication = DemandeDeCritiquePublication()

    # returns queryset of tickets

    return render(request, "demande_de_critique.html", context={"demande": publication})


@login_required
def repondre_ticket(request, ticket_id):
    ticket = Ticket.objects.get(id=ticket_id)
    if request.method == "POST":

        publication = ReviewForm(request.POST, request.FILES)
        if [publication.is_valid()]:
            review = publication.save(commit=False)
            review.user = request.user
            review.ticket = ticket
            review.save()

            return redirect("Home")
        else:
            print(publication.errors)
            print(request.POST)
    else:
        publication = ReviewForm()

    # returns queryset of tickets

    return render(
        request,
        "fenêtre_repondre.html",
        context={"ticket": ticket, "reponse": publication},
    )


@login_required
def afficher_abonnement(request):

    return render(request, "abonnement.html", context={})


class Subscriptions(View):
    """View for subscriptions page"""

    @method_decorator(login_required(login_url="/auth/"))
    def get(self, request):
        user_follows_form = UserFollowForm()
        actual_user = request.user
        user_subscriptions = list(UserFollows.objects.filter(user=actual_user))

        subscribers = [
            user_follow.user
            for user_follow in UserFollows.objects.filter(followed_user=actual_user)
        ]

        error_message = (
            request.GET.get("error_message")
            if request.GET.get("error_message") != "None"
            else None
        )
        validation_message = (
            request.GET.get("validation_message")
            if request.GET.get("validation_message") != "None"
            else None
        )
        followed_user = (
            request.GET.get("followed_user")
            if request.GET.get("followed_user") != "None"
            else None
        )
        if error_message is not None:
            error_message = _MESSAGES[error_message].format(username=followed_user)
        else:
            error_message = None
        if validation_message is not None:
            validation_message = _MESSAGES[validation_message].format(
                username=followed_user
            )
        else:
            validation_message = None

        return render(
            request,
            "abonnement.html",
            context={
                "user_follows_form": user_follows_form,
                "subscriptions": user_subscriptions,
                "subscribers": subscribers,
                "error_message": error_message,
                "validation_message": validation_message,
                "UserFollowsForm": user_follows_form,
            },
        )

    @method_decorator(login_required(login_url="/auth/"))
    def post(self, request):
        error_message = None
        validation_message = None
        actual_user = request.user
        followed_user_username = request.POST.get("followed_user", False)
        print(request.POST)

        if (
            not get_user_model()
            .objects.filter(username=followed_user_username)
            .exists()
        ):
            error_message = "unknown_user"
        elif followed_user_username == actual_user.username:
            error_message = "do_not_follow_yourself"
        else:
            followed_user_id = (
                get_user_model().objects.get(username=followed_user_username).id
            )
            follows_form = UserFollowForm(
                {"user": actual_user, "followed_user": followed_user_id}
            )
            if follows_form.is_valid():
                follows_form = follows_form.save(commit=False)
                follows_form.user = request.user
                follows_form.save()

                validation_message = "subscription_succes"
            else:
                error_message = "already_following"

        query = {
            "error_message": error_message,
            "validation_message": validation_message,
            "followed_user": followed_user_username,
        }
        query_string = urlencode(query)

        return redirect(f"/abonnement/?{query_string}")


class DeleteSubscription(View):
    """Link to delete subscription"""

    @method_decorator(login_required(login_url="/auth/"))
    def get(self, request, followed_user_id):
        actual_user = request.user
        followed_user = get_user_model().objects.get(id=followed_user_id)
        subscription_to_delete = UserFollows.objects.get(
            user=actual_user, followed_user=followed_user
        )
        subscription_to_delete.delete()
        validation_message = "stopped_subscription"

        query = {
            "validation_message": validation_message,
            "followed_user": followed_user.username,
        }
        query_string = urlencode(query)

        return redirect(f"/abonnement/?{query_string}")
