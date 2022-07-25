from dataclasses import field, fields
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import EmailField 
from django.contrib.auth import get_user_model


from django import forms

class CreationCompte(UserCreationForm):

    email = forms.EmailField(label="email")


    
    
    class Meta():
        model = get_user_model()
        fields = ['username','last_name','first_name','password1','password2','email']
        widgets = {
                'username': forms.TextInput(attrs={'class' : "form-control"}),
                'last_name': forms.TextInput(attrs={'class' : "form-control"}),
                'first_name': forms.TextInput(attrs={'class' : "form-control"}),
                 'password1': forms.TextInput(attrs={'class' : "form-control"}),
                'password2': forms.TextInput(attrs={'class' : "form-control"}),
               'email': forms.TextInput(attrs={'class' : "form-control"}),}
                
                
               
  


