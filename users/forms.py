from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth import get_user_model




User = get_user_model()


###
# user forms
###

class SignUpForm(UserCreationForm):
    '''
    developer signup form
    '''
    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name',
                  )
