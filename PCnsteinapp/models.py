from django.db import models
from django.contrib.auth.models import User

import datetime

#
#
class Manufacturer(models.Model):
	name = models.CharField(primary_key=True, max_length=35)
	desc = models.TextField(blank=True, null=True)

	def __unicode__(self):
		return self.name

#
#
class Category(models.Model):
	name = models.CharField(max_length=20, primary_key=True)

	def __unicode__(self):
		return self.name
#
#
class Component(models.Model):
	ref = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=75)
	desc = models.TextField(blank=True, null=True)
	avgprice = models.DecimalField(max_digits=7, decimal_places=3, blank=True)
	img = models.ImageField(upload_to='static/img', blank=True, null=True)
	category = models.ForeignKey(Category, blank=True, null=True,
													on_delete=models.SET_NULL)
	createdby = models.ForeignKey(User, blank=True, null=True, 
													on_delete=models.SET_NULL)

	def __unicode__(self):
		return self.name + ' - ' + self.ref

#
#
class Review(models.Model):
	RATING_CHOICES = ((1,'one'), (2, 'two'), (3, 'three'), (4, 'four'), 
		(5, 'five'))
	rating = models.PositiveSmallIntegerField('Rating (stars)', blank=False,
		default=3, choices=RATING_CHOICES)
	comment = models.TextField(blank=True, null=True)
	user = models.ForeignKey(User)	
	date = models.DateField(default=datetime.date.today)

	class Meta:
		abstract = True

#
#
class ComponentReview(Review):
	component = models.ForeignKey(Component)

	def __unicode__():
		return str(component) + " - " + str(user) + " : " + str(rating)

#
#
class OperatingSystem(models.Model):
	name = models.CharField(max_length=20, primary_key=True)

	def __unicode__(self):
		return self.name

#
#
class SupportedBy(models.Model):
	component = models.ForeignKey(Component)
	os = models.ForeignKey(OperatingSystem)
	minversion = models.CharField(max_length=20)
	maxversion = models.CharField(max_length=20)
	details = models.TextField(blank=True)

	def __unicode__(self):
		return str(self.component) + ' supported by ' + str(self.os)

#
#
class CMadeBy(models.Model):
	component = models.ForeignKey(Component, blank=False, unique=True)
	manufacturer = models.ForeignKey(Manufacturer, blank=False)

	def __unicode__(self):
		return str(self.component) + ' made by ' + str(self.manufacturer)

#
#
class OSMadeBy(models.Model):
	os = models.ForeignKey(OperatingSystem, unique=True)
	manufacturer = models.ForeignKey(Manufacturer)

	def __unicode__(self):
		return str(self.os) + ' made by ' + str(self.manufacturer)