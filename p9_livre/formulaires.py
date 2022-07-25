from dataclasses import field, fields
from email.mime import image
from urllib import request
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField, ModelForm 
from django.contrib.auth import get_user_model
from .models import Ticket , Review, UserFollows

from django import forms


class DemandeDeCritiquePublication(forms.ModelForm):



    class Meta:
        model = Ticket
        fields = ('title','description','image',)
        widgets = {
                'title': forms.TextInput(attrs={'class' : "form-control"}),
                'description': forms.Textarea(attrs={'class' : "form-control"}),

                
               }


class RepondreCritique(forms.ModelForm):



    class Meta:
        model = Ticket
        fields = ('title','description',)
        widgets = {
                'title': forms.TextInput(attrs={'class' : "form-control"}),
                'description': forms.Textarea(attrs={'class' : "form-control"}),

                
               }

class DeleteTicketForm(forms.Form):
    delete_ticket = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class ReviewForm(forms.ModelForm):
    review = forms.BooleanField(widget=forms.HiddenInput, initial=True)
    
    class Meta:
        model = Review
        fields = ['rating','description', ]
        widgets = {

            'rating': forms.RadioSelect(
                choices=[
                    (0, '0'),
                    (1, '1'),
                    (2, '2'),
                    (3, '3'),
                    (4, '4'),
                    (5, '5'),
                ],
                attrs={"required": True}
                ),
            'description': forms.Textarea(attrs={'class' : "form-control"}),
        }


class DeleteReviewForm(forms.Form):
    delete_review = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class DeleteFollowedUserForm(forms.Form):
    delete_follow = forms.BooleanField(widget=forms.HiddenInput, initial=True)


class UserFollowForm(forms.ModelForm):
    

    class Meta:
        model = UserFollows
        fields = ['followed_user']
        widgets = {
            'followed_user': forms.TextInput(attrs={'placeholder': 'Nom d\'utilisateur'})
        }       