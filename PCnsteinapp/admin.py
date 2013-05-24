from django.contrib import admin
from PCnsteinapp.models import Manufacturer, Component, OperatingSystem, \
								SupportedBy, OSMadeBy, Category, \
								ComponentReview, UserProfile

admin.site.register(Manufacturer)
admin.site.register(Component)
admin.site.register(OperatingSystem)
admin.site.register(SupportedBy)
admin.site.register(OSMadeBy)
admin.site.register(Category)
admin.site.register(ComponentReview)
admin.site.register(UserProfile)