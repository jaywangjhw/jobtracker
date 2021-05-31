from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


# Source Citation: Using the allauth package, we wanted to ensure that an existing user to our site
# would still be able to login using Google. To handle these cases, we found a solution at:
# https://stackoverflow.com/questions/24357907/django-allauth-facebook-redirects-to-signup-when-retrieved-email-matches-an-exis
# which is implemented here.
@receiver(pre_social_login)
def check_for_existing_user(sender, request, sociallogin, **kwargs):
    ''' When a user logs in via Google, allauth sends the pre_social_login signal.
    	We want to check if this user's email is already in our database of existing users.
    	If so, the user will be logged in with that existing account. 
    	If a user doesn't exist with this email, the allauth social login flow continues as
    	normal. In that case a new User will be created with their Google email, and their
    	first name (as returned by Google) will be set as their username.
    '''
    gmail_email = sociallogin.account.extra_data['email']
    # Get all existing users from our db with this email address
    existing_users = User.objects.filter(email=gmail_email)
    if existing_users:
        # If we have an existing user with this email address, log them in
        # Note: If multiple accounts exist with this email address, only the first user is going
        # to be connected to this social account.
        perform_login(request, existing_users[0], email_verification='optional')
        # Redirect the user to the home page
        raise ImmediateHttpResponse(redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id)))
