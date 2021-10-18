from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from users.models import Profile
from PIL import Image
from crispy_forms.helper import FormHelper


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100 ,label='Enter FirstName')
    last_name = forms.CharField(max_length=100 ,label='Enter LastName')
    email = forms.EmailField(max_length=150, help_text='Enter your Email')
    helper = FormHelper()

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username','email', 'password1', 'password2')

class ProfileUpdateForm(forms.ModelForm):
    helper = FormHelper()
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','enrolled','finished']

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100 ,label='Enter FirstName',required=False)
    last_name = forms.CharField(max_length=100 ,label='Enter LastName',required=False)
    # username = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['first_name','last_name', 'username', 'email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user','enrolled','finished']