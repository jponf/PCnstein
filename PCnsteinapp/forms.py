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

#
#
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = models.UserProfile
        exclude = ['user']

#
#
class SupportedByForm(forms.ModelForm):
    class Meta:
        model = models.SupportedBy
        exclude = ['component']
