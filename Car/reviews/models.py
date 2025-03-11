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

# Car Table
class Car(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name="cars", null=True, blank=False)
    variant = models.CharField(max_length=50, help_text="e.g., VXI, ZXI, ZXI+", null=True, blank=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(null=True, blank=False)
    category = models.CharField(max_length=50, help_text="e.g., SUV, Sedan, Hatchback", null=True, blank=False)
    engine_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20,choices=[("Manual","Manual"),("Automatic","Automatic")] )
    mileage = models.DecimalField(max_digits=10, decimal_places=2, help_text="in km/l")
    horse_power = models.DecimalField(max_digits=10, decimal_places=2, help_text="in HP")
    torque = models.DecimalField(max_digits=10, decimal_places=2, help_text="in Nm")
    pros = models.TextField(null=True, blank=True)
    cons = models.TextField(null=True, blank=True)
    image_file = models.ImageField(upload_to='car_images/', help_text="Upload an image of the car", null=True, blank=True)
    
    # Fixed created_at and updated_at
    created_at = models.DateTimeField(auto_now_add=True)  # Now correctly sets when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Updates automatically when the object is saved

    featured = models.BooleanField(default=False, help_text="Mark as featured car")

    @property
    def price_in_lakhs(self):
        return round(self.price / 100000, 2)

    def __str__(self):
        return f"{self.car_model.brand.bname} {self.car_model.model_name} {self.variant} ({self.car_model.year})"

    class Meta:
        ordering = ['car_model', 'variant']
        verbose_name_plural = "Car"

# Review Model
class Review(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=3)
    review_text = models.TextField(help_text="Write your review here")
    created_at = models.DateTimeField(auto_now_add=True)  # Fixed to store correct timestamp

    def __str__(self):
        return f"{self.user.username} - {self.car.car_model.model_name} ({self.rating}⭐)"

    class Meta:
        ordering = ['-created_at']
        
