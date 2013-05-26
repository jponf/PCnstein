# -*- coding: utf-8 -*-

from rest_framework import serializers
from rest_framework.fields import CharField
from rest_framework.relations import HyperlinkedRelatedField
import models

#
#
class UserSerializer(serializers.HyperlinkedModelSerializer):
    username = CharField(read_only=True)

    class Meta:
        model = models.User
        fields = ('username',)

#
#
class ComponentSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = models.Component
        fields = ('ref', 'name', 'desc', 'avgprice', 'img', 'manufacturer',
                    'createdby', 'category',)

#
#
class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Category
        fields = ('name',)

#
#
class ManufacturerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Manufacturer
        fields = ('name', 'desc')

#
#
class OperatingSystemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.OperatingSystem
        fields = ('name',)

#
#
class SupportedBySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.SupportedBy
        fields = ('id', 'component', 'os', 'minversion', 'maxversion', 
            'details')