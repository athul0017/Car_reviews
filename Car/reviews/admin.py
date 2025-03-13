from django.contrib import admin
from .models import Brand, CarGallery, CarModel, Car, Review

admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Review)

class CarGalleryAdmin(admin.ModelAdmin):
    list_display = ('car__car_model__model_name', 'created_at', 'updated_at')
    search_fields = ["car__car_model__model_name", ]

admin.site.register(CarGallery, CarGalleryAdmin)


