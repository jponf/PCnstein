# -*- coding: utf-8 -*-

from django import forms

import models

#
#
class ModifyComponentForm(forms.ModelForm):
    class Meta:
        model = models.Component
        exclude = 'ref'

#
#
class ModifyManufacturerForm(forms.ModelForm):
    class Meta:
        model = models.Manufacturer
        exclude = 'name'

