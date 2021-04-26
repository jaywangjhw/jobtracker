from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User


class Company(models.Model):
	INDUSTRY_CHOICES = [
		('tech', 'Tech'),
		('ecommerce', 'Ecommerce'), 
		('healthcare', 'Healthcare'),
		('pharma', 'Pharmaceutical'),
		('aerospace', 'Aerospace'),
		('fintech', 'FinTech'),
		('nonprofit', 'Nonprofit'),
		('defense', 'Defense'),
		('other', 'Other'),
	]
	
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1)
	name = models.CharField(max_length=100)
	careers_url = models.URLField(max_length=300, null=True)
	industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=100, null=True)

	def __str__(self):
		"""String for representing the Company as the Company name"""
		return self.name

	def get_absolute_url(self):
		return reverse('jobs-company-detail', kwargs={'pk': self.pk})



# Need to add dependencies on User and Source class
class Position(models.Model):

	INDUSTRY_SKILL = [
		('Java', 'Java'), 
		('C++', 'C++'),
		('Algorithm Design', 'Algorithm Design'), 
		('Object Oriented', 'Object Oriented'), 
		('Kubernetes', 'Kubernetes')
	]

	# Columns in Position table
	position_title = models.CharField(max_length=100)
	position_url = models.URLField(max_length=300, null=True)
	date_opened = models.DateField(null=True)
	date_closed = models.DateField(null=True, blank=True, default='')
	skills = models.CharField(choices=INDUSTRY_SKILL, max_length=100) # Need to look into multiple selection
	job_description = models.TextField(null=True)

	def __str__(self):
		"""String for representing the Position as the Position name"""
		return self.position_title

	def get_absolute_url(self):
		return reverse('jobs-list-positions')

class Account(models.Model):
	user = models.OneToOneField(
		User,
        on_delete=models.CASCADE
    )

	def __str__(self):
		return self.user.username


def post_new_user_created_signal(sender, instance, created, **kwargs):
	''' Every time a new user registers for the site and a new User
		is created in the db, this function gets passed to the post_save
		signal, to automatically create an Account for that new User.
	'''
	if created:
		Account.objects.create(user=instance)


# Listens for new User creation
post_save.connect(post_new_user_created_signal, sender=User)
