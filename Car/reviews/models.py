from django.db import models

class Car(models.Model):
    BRAND_CHOICES = (
        ('Toyota', 'Toyota'),
        ('Honda', 'Honda'),
        ('Ford', 'Ford'),
        ('Suzuki', 'Suzuki'),
        ('Hyundai', 'Hyundai'),
        ('Skoda', 'Skoda'),
        ('BMW', 'BMW'),
        # Add more brands as needed
    )

    MODEL_CHOICES = (
        ('Corolla', 'Corolla'),
        ('Civic', 'Civic'),
        ('Mustang', 'Mustang'),
        ('Celerio', 'Celerio'),
        ('i20', '120'),
        ('Kylaq', 'Kylaq'),
        ('3 Series', '3 Series'),
        # Add more models as needed
    )

    brand = models.CharField(max_length=30, choices=BRAND_CHOICES)
    model = models.CharField(max_length=30, choices=MODEL_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    engine_type = models.CharField(max_length=20)
    transmission = models.CharField(max_length=20)
    mileage = models.DecimalField(max_digits=10, decimal_places=2, help_text="in km/l")  # Added help_text
    horse_power = models.DecimalField(max_digits=10, decimal_places=2, help_text="in HP")  # Added help_text
    torque = models.DecimalField(max_digits=10, decimal_places=2, help_text="in Nm")  # Added help_text
    pros = models.TextField()
    cons = models.TextField()

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"  # Updated to include year

    class Meta:
        ordering = ['brand', 'model']
        verbose_name_plural = "Cars"
        


 

# class Reviews(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
#     car = models.ForeignKey('Car', on_delete=models.CASCADE)  
#     rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  
#     review_text = models.TextField()  
#     created_at = models.DateTimeField(auto_now_add=True)


