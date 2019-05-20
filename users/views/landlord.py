from django.views.generic import CreateView, DetailView, UpdateView, TemplateView
from django.contrib.auth import get_user_model
from django.shortcuts import redirect, render

from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator



from ..forms import (
    SignUpForm, )



User = get_user_model()

#developer sign up view
class LandlordSignupView(CreateView):
    '''
    handle developer signup
    '''
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'
    success_url = '/users/accounts/login/'
    

    #add user_type to *kwargs
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'Land Lord'
        return super().get_context_data(**kwargs)

    #overwrite form_valid method to and assign user.is_developer=True
    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_developer = True
        user.save()
        return super().form_valid(form)

        

