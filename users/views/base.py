from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.views.generic import TemplateView, UpdateView, RedirectView
from django.contrib.auth.views import PasswordChangeView, PasswordResetView

from django.utils.decorators import method_decorator




from django.urls import reverse_lazy



User = get_user_model()

def is_person(func):
    '''
    Decorator for views that checks that the logged in user is a developer,
    redirects to the log-in page if necessary.
    '''
    
    def check_and_call(request, *args, **kwargs):
        #user = request.user
        #print user.id
        slug = kwargs["slug"]
        user = User.objects.get(slug=slug)
        if not (user == request.user): 
            return HttpResponse("It is not yours ! You are not permitted !",
                        content_type="text/html", status=403)
        return func(request, *args, **kwargs)
    return check_and_call

class UserSignUpView(TemplateView):
    template_name = 'registration/signup.html'

@method_decorator([is_person], name='dispatch')
class UserChangePasswordView(PasswordChangeView):
    '''
    change password view
    '''
    template_name = 'registration/change_password.html' 
    success_url = reverse_lazy('update_success')         

    
@method_decorator([is_person], name='dispatch')
class UserPasswordResetView(PasswordResetView):
    '''
    reset password view
    '''
    template_name = 'registration/password_reset_form.html'
    
    
@method_decorator([is_person], name='dispatch')
class UserDetailsUpdateView(UpdateView):
    '''
    user details update view
    '''

    model = User
    template_name = 'registration/user_details_update.html'
    
    success_url = reverse_lazy('update_redirect')
    fields = ('first_name', 'last_name', )

    def get_context_data(self, **kwargs):
        return super().get_context_data(**kwargs)

class UpdateSuccessRedirect(RedirectView):
    '''
    redirect from user details change
    '''
    permanent = False
    query_string = True          
    

    def get_redirect_url(self, *args, **kwargs):
        
        user = self.request.user
        
        if user.is_developer:
            profile = get_object_or_404(DeveloperProfile, user=self.request.user)
            kwargs['slug']=profile.slug
            self.pattern_name = 'developer_profile'
            
        elif user.is_employer:
            profile = get_object_or_404(EmployerProfile, user=self.request.user)
            kwargs['slug']=profile.slug
            self.pattern_name = 'employer_profile'

        else:
            raise Exception('We encountered a problem getting back to your profile !')
        
        return super().get_redirect_url(*args, **kwargs)
 
class UpdateSuccessView(TemplateView):
    template_name = 'registration/update_success.html'