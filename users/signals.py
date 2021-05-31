from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
import json

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)



# Source from https://stackoverflow.com/questions/24357907/django-allauth-facebook-redirects-to-signup-when-retrieved-email-matches-an-exis
class MyLoginAccountAdapter(DefaultAccountAdapter):
    '''
    Overrides allauth.account.adapter.DefaultAccountAdapter.ajax_response
    '''

    def get_login_redirect_url(self, request):
        '''
        Redirects url after authentication
        '''
        if request.user.is_authenticated():
            return settings.LOGIN_REDIRECT_URL.format(
                id=request.user.id)
        else:
            return "/"


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login
    '''
    def pre_social_login(self, request, sociallogin):
        pass

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    ''' Fixes issue where user's email retrieved is different from existing email in the database
    '''
    email_address = sociallogin.account.extra_data['email']
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))
