from django.db import models
from django.db.models.signals import post_save
from django.urls import reverse
from django.contrib.auth.models import User
from users.models import Document


class Skill(models.Model):

	# Columns in Skill table
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)

	skill_name = models.CharField(max_length=100)

	def __str__(self):
		"""String for representing the Skill as the Skill name"""
		return self.skill_name


class Company(models.Model):
	INDUSTRY_CHOICES = [
		('tech', 'Tech'),
		('ecommerce', 'Ecommerce'),
		('gaming', 'Gaming'), 
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
	careers_url = models.URLField(max_length=1000, null=True, blank=True)
	industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=100, null=True, blank=True)

	def num_company_apps(self):
		num_apps = 0
        
		for position in self.position_set.all():
			num_apps += position.num_apps()

		return num_apps

	def __str__(self):
		"""String for representing the Company as the Company name"""
		return self.name


class Position(models.Model):

	# Columns in Position table
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
	company = models.ForeignKey(
		Company,
		on_delete=models.CASCADE
		)
	position_title = models.CharField(max_length=100)
	position_url = models.URLField(max_length=1000, null=True)
	date_opened = models.DateField(null=True)
	date_closed = models.DateField(null=True, blank=True, default='')
	skills = models.ManyToManyField(Skill, blank=True)
	job_description = models.TextField(null=True)

	def num_apps(self):
		return Application.objects.filter(position=self).count()

	def __str__(self):
		"""String for representing the Position as the Position name"""
		return self.position_title + ' - ' + self.company.name

	def get_absolute_url(self):
		return reverse('jobs-list-positions')


class Contact(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(null=True, blank=True, max_length=128)
	phone_number = models.IntegerField(null=True, blank=True)
	notes = models.TextField(null=True, blank=True)
	
	def get_absolute_url(self):
		return reverse('jobs-contacts')

	def __str__(self):
		"""String for representing a Contact as their first and last names"""
		return self.first_name + ' ' + self.last_name


class Account(models.Model):
	user = models.OneToOneField(
		User,
        on_delete=models.CASCADE
    	)

	def __str__(self):
		return self.user.username


class Application(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
	position = models.ForeignKey(
		Position,
		on_delete=models.CASCADE
		)
	resume = models.ForeignKey(
		Document,
		on_delete=models.SET_NULL,
		null=True,
		blank=True)
	date_started = models.DateField(null=True, blank=True)
	date_submitted = models.DateField(null=True, blank=True)
	email_used = models.EmailField(null=True, blank=True, max_length=128)
	offer = models.BooleanField()
	accepted = models.BooleanField()
	notes = models.TextField(null=True, blank=True)

	def get_absolute_url(self):
		return reverse('jobs-list-applications')

	def __str__(self):
		company = self.position.company.name
		job_title = self.position.position_title
		return company + ' - ' + job_title


class Interview(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
	application = models.ForeignKey(
		Application,
		on_delete=models.CASCADE
		)
	date = models.DateField(null=True, blank=True)
	time = models.CharField(null=True, blank=True, max_length=10)
	location = models.CharField(null=True, blank=True, max_length=256)
	virtual_url = models.CharField(null=True, blank=True, max_length=512)
	complete = models.BooleanField()
	notes = models.TextField(null=True, blank=True)


class Assessment(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
	application = models.ForeignKey(
		Application,
		on_delete=models.CASCADE
		)
	date = models.DateField(null=True, blank=True)
	time = models.CharField(null=True, blank=True, max_length=10)
	virtual_url = models.CharField(null=True, blank=True, max_length=512)
	complete = models.BooleanField()
	notes = models.TextField(null=True, blank=True)


class Communication(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		default=1
		)
	application = models.ForeignKey(
		Application,
		on_delete=models.CASCADE
		)
	contact = models.ForeignKey(
		Contact,
		on_delete=models.CASCADE
		)
	date = models.DateField(null=True, blank=True)
	method = models.CharField(choices=[('phone','Phone'), ('email','Email'), ('meeting','Meeting'),], max_length=100, null=True)
	notes = models.TextField(null=True, blank=True)

	def __str__(self):
		company = self.application.position.company.name
		job_title = self.application.position.position_title
		return self.contact.last_name + '-' + company + '-' + job_title
	
	def get_absolute_url(self):
		return reverse('jobs-list-communications')
