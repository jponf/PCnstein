from django.db import models

# Create your models here.

#
#
class Manufacturer(models.Model):
	name = models.CharField(max_length=35)
	ref = models.CharField(max_length=20)
	desc = models.TextField()

#
#
class Component(models.Model):
	ref = models.CharField(max_length=20, primary_key=True)
	name = models.CharField(max_length=75)
	desc = models.TextField()
	avg_price = models.DecimalField(max_digits=7, decimal_places=3)

#
#
class OperatingSystem(models.Model):
	name = models.CharField(max_length=20)

#
#
class SupportedBy(models.Model):
	component = models.ForeignKey(Component)
	os = models.ForeignKey(OperatingSystem)
	min_version = models.CharField(max_length=20)
	max_version = models.CharField(max_length=20)

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