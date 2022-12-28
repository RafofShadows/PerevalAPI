from django.contrib import admin

# Register your models here.
from .models import User, Coords, Area, Image, PassData, Level, PerevalImages

admin.site.register(User)
admin.site.register(Coords)
admin.site.register(Area)
admin.site.register(Image)
admin.site.register(PassData)
admin.site.register(Level)
admin.site.register(PerevalImages)
