from django.db import models


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
	
	name = models.CharField(max_length=100)
	careers_url = models.URLField(max_length=300, null=True)
	industry = models.CharField(choices=INDUSTRY_CHOICES, max_length=100, null=True)

	def __str__(self):
		"""String for representing the Company as the Company name"""
		return self.name



# Need to add dependencies on User and Source class
class Position(models.Model):

	INDUSTRY_SKILL = [
		('java', 'Java'), 
		('c++', 'C++'),
		('algorithm', 'Algorithm Design'), 
		('object', 'Object Oriented'), 
		('kubernetes', 'Kubernetes')
	]

	# Columns in Position table
	position_title = models.CharField(max_length=100)
	position_url = models.URLField(max_length=300, null=True)
	date_opened = models.DateField(null=True)
	date_closed = models.DateField(null=True, blank=True, default='')
	skills = models.CharField(choices=INDUSTRY_SKILL, max_length=100) # Need to look into multiple selection
	job_description = models.TextField(null=True)

class Account(models.Model):

	def __str__(self):
		return self.name
