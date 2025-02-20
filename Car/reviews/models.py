from django.db import models

# Create your models here.
class Car(models.Model):
    brand =models.CharField(max_length=30)
    model =models.CharField(max_length=30)
    price =models.DecimalField(max_digits=10,decimal_places=2)
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])
    engine_type=models.CharField(max_length=20)
    transmission =models.CharField(max_length=20)
    mileage =models.DecimalField(max_digits=10,decimal_places=2)
    horse_power =models.DecimalField(max_digits=10,decimal_places=2)
    torque =models.DecimalField(max_digits=10,decimal_places=2)
    pros = models.TextField()  
    cons = models.TextField()



# class Reviews(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE) 
#     car = models.ForeignKey('Car', on_delete=models.CASCADE)  
#     rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])  
#     review_text = models.TextField()  
#     created_at = models.DateTimeField(auto_now_add=True)


