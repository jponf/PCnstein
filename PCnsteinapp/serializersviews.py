# -*- coding: utf-8 -*-

from rest_framework import generics


import models
import serializers

#
#
class ComponentCreateAPIView(generics.ListCreateAPIView):
    model = models.Component
    serializer_class = serializers.ComponentSerializer

#
#
class ComponentUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = models.Component
    serializer_class = serializers.ComponentSerializer