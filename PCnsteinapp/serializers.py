# -*- coding: utf-8 -*-

from rest_framework import serializers

import models

#
#
class ComponentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = models.Component
        fields = ('ref', 'name', 'desc', 'avgprice', 'img', 'category')

#
#
class MadeBySerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = models.CMadeBy
		fields = ('component', 'manufacturer')