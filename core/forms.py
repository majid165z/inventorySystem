from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth import get_user_model

class SignUpForm(UserCreationForm):
    warehouse_keeper = forms.BooleanField(required=False)
    name = forms.CharField(label='Name',required=True)
    last_name = forms.CharField(label='Last Name',required=True)
    class Meta:
        model = get_user_model() 
        fields = ('username', 'password1', 'password2','warehouse_keeper','technical')

class UserUpdateForm(UserChangeForm):
    password = None

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'warehouse_keeper','technical' ]
        widgets = {
            'username': forms.TextInput(attrs={'readonly': 'readonly'}),
            'email': forms.TextInput(attrs={'readonly': 'readonly'})
        }