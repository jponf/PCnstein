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
    def __init__(self, *args, **kwargs):
        super(SupportedByForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False

    class Meta:
        model = models.SupportedBy
        exclude = ['component', 'details']

#
#
class CMadeByForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CMadeByForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].required = False

    class Meta:
        model = models.CMadeBy
        exclude = ['component']