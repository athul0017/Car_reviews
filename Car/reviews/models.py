from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Brand Model (e.g., Maruti Suzuki, Toyota, Ford)
class Brand(models.Model):
    bname = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.bname

# Car Model Table (e.g., Swift, Celerio, Fortuner)
class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="models")
    model_name = models.CharField(max_length=50)
    year = models.IntegerField()

    def __str__(self):
        return f"{self.brand.bname} {self.model_name} ({self.year})"

# Car Table (Actual cars available for sale)
class Car(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars", null=True, blank=False)  # Linked to CarModel
    variant = models.CharField(max_length=50, help_text="e.g., VXI, ZXI, ZXI+", null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, help_text="e.g., SUV, Sedan, Hatchback", null=True, blank=False)
    # rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    engine_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20, choices=[("Manual", "Manual"), ("Automatic", "Automatic")])
    mileage = models.DecimalField(max_digits=10, decimal_places=2, help_text="in km/l")
    horse_power = models.DecimalField(max_digits=10, decimal_places=2, help_text="in HP")
    torque = models.DecimalField(max_digits=10, decimal_places=2, help_text="in Nm")
    pros = models.TextField(null=True, blank=True)
    cons = models.TextField(null=True, blank=True)
    image_url = models.URLField(max_length=200, help_text="URL of the car image", null=True, blank=True)
    created_at = models.DateTimeField(default=now, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
   

    def __str__(self):
        return f"{self.car_model.brand.bname} {self.car_model.model_name} {self.variant} ({self.car_model.year})"
    
    
    

    class Meta:
        ordering = ['car_model', 'variant']
        verbose_name_plural = "Cars"


class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews")  # Each review is linked to a Car
    user = models.ForeignKey(User, max_length=100,on_delete=models.CASCADE )  # Name of the reviewer
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)  # Rating from 1-5
    review_text = models.TextField(help_text="Write your review here")  # Review content
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when review is created

    def __str__(self):
        return f"{self.user.username} - {self.car.car_model.model_name} ({self.rating}⭐)"

    class Meta:
        ordering = ['-created_at']  # Latest reviews first        
