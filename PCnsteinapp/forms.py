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
class CreateComponentForm(forms.ModelForm):
	class Meta:
		model = models.Component
		exclude = ['createdby']

#
#
class CreateReviewForm(forms.ModelForm):
	class Meta:
		model = models.ComponentReview
		exclude = ['user', 'component']
