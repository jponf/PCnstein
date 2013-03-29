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
	category = models.CharField(max_length=25)

	def __unicode__(self):
		return self.name + ' - ' + self.ref

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
		return str(self.component) + ' supported by ' + str(self.os)

#
#
class CMadeBy(models.Model):
	component = models.ForeignKey(Component)
	manufacturer = models.ForeignKey(Manufacturer)

	def __unicode__(self):
		return str(self.component) + ' made by ' + str(self.manufacturer)

#
#
class OSMadeBy(models.Model):
	os = models.ForeignKey(OperatingSystem)
	manufacturer = models.ForeignKey(Manufacturer)

	def __unicode__(self):
		return str(self.os) + ' made by ' + str(self.manufacturer)

#
#
class CPU(models.Model):
	ref = models.ForeignKey(Component)
	family = models.CharField(max_length=25)
	socket = models.CharField(max_length=15)
	arch = models.IntegerField()				# in bits
	cores = models.IntegerField()				
	clock_speed = models.FloatField()			# in Ghz
	lithograpy = models.IntegerField()			# in nm

	def __unicode__(self):
		return str(self.ref)

#
#
class HardDisk(models.Model):
	ref = models.ForeignKey(Component)
	rpm = models.IntegerField()
	interface = models.CharField(max_length=10)
	buffer_size = models.IntegerField()
	transfer_speed = models.DecimalField(max_digits=3, decimal_places=1)
	size = models.DecimalField(max_digits=2, decimal_places=1)

	def __unicode__(self):
		return str(self.ref)