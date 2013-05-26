# -*- coding: utf-8 -*-

from rest_framework import generics


import models
import serializers

#
#
class ComponentListCreateAPIView(generics.ListCreateAPIView):
    model = models.Component
    serializer_class = serializers.ComponentSerializer

#
#
class ComponentUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    model = models.Component
    serializer_class = serializers.ComponentSerializer

#
#
class CategoryListAPIView(generics.ListAPIView):
	model = models.Category
	serializer_class = serializers.CategorySerializer

#
#
class CategoryRetrieveAPIView(generics.RetrieveAPIView):
	model = models.Category
	serializer_class = serializers.CategorySerializer

#
#
class ManufacturerListAPIView(generics.ListAPIView):
	model = models.Manufacturer
	serializer_class = serializers.ManufacturerSerializer

#
#
class ManufacturerRetrieveAPIView(generics.RetrieveAPIView):
	model = models.Manufacturer
	serializer_class = serializers.ManufacturerSerializer

#
#
class UserListAPIView(generics.ListAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer

#
#
class UserRetrieveAPIView(generics.RetrieveAPIView):
	model = models.User
	serializer_class = serializers.UserSerializer

#
#
class OperatingSystemListAPIView(generics.ListAPIView):
	model = models.OperatingSystem
	serializer_class = serializers.OperatingSystemSerializer

#
#
class OperatingSystemRetrieveAPIView(generics.RetrieveAPIView):
	model = models.OperatingSystem
	serializer_class = serializers.OperatingSystemSerializer

#
#
class SupportedByListAPIView(generics.ListAPIView):
	model = models.SupportedBy
	serializer_class = serializers.SupportedBySerializer

#
#
class SupportedByRetrieveAPIView(generics.RetrieveAPIView):
	model = models.SupportedBy
	serializer_class = serializers.SupportedBySerializer