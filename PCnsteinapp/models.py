from django.db import models

# Create your models here.

#
#
class Manufacturer(models.Model):
	name = models.CharField(max_length=35)
	desc = models.TextField()

	def __unicode__(self):
		return self.name


#
#
class Component(models.Model):
	ref = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=75)
	desc = models.TextField()
	avg_price = models.DecimalField(max_digits=7, decimal_places=3)
	img = models.ImageField(upload_to='static/img')
	category = models.CharField(max_length=30)

	def __unicode__(self):
		return self.name + ' - ' + ref

#
#
class OperatingSystem(models.Model):
	name = models.CharField(max_length=20)

	def __unicode__(self):
		return self.name

#
#
class SupportedBy(models.Model):
	component = models.ForeignKey(Component)
	os = models.ForeignKey(OperatingSystem)
	min_version = models.CharField(max_length=20)
	max_version = models.CharField(max_length=20)

	def __unicode__(self):
		return str(component) + ' supported by ' + str(os)

#
#
class CMadeBy(models.Model):
	component = models.ForeignKey(Component)
	manufacturer = models.ForeignKey(Manufacturer)	

#
#
class OSMadeBy(models.Model):
	os = models.ForeignKey(OperatingSystem)
	manufacturer = models.ForeignKey(Manufacturer)

#
# Component Generalization
class CPU(models.Model):
	family = models.CharField(max_length=25)
	socket = models.CharField(max_length=15)
	arch = models.IntegerField()
	cores = models.IntegerField()
	clock_speed = models.FloatField()
	arch_size = models.IntegerField()