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