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

    def save(self):
        p = super().save()

        img = Image.open(p.profile_pic.path) # Open image
        
        # resize image
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size) # Resize image
            img.save(p.profile_pic.path) # Save it again and override the larger image
