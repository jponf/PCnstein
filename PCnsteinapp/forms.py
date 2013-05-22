# -*- coding: utf-8 -*-

from django import forms

import models

#
#
class ModifyComponentForm(forms.ModelForm):
    class Meta:
        model = models.Component
        exclude = ['ref', 'createdby']

#
#
class ModifyManufacturerForm(forms.ModelForm):
    class Meta:
        model = models.Manufacturer
        exclude = ['name']

#
#
class CreateComponentForm(forms.ModelForm):
	class Meta:
		model = models.Component
		exclude = ['createdby']

