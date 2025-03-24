from django.contrib import admin
from .models import Brand, CarGallery, CarModel, Car, Review

admin.site.register(Brand)
admin.site.register(CarModel)
admin.site.register(Car)
admin.site.register(Review)

class CarGalleryAdmin(admin.ModelAdmin):
    list_display = ('get_car_model', 'created_at', 'updated_at')
    search_fields = ['car__car_model__model_name']

    def get_car_model(self, obj):
        return obj.car.car_model.model_name
    get_car_model.short_description = "Car Model"

admin.site.register(CarGallery, CarGalleryAdmin)
