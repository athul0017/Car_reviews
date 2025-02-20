from django.db import models

# Create your models here.
class Car(models.Model):
    brand =models.CharField(max_length=30)
    model =models.CharField(max_length=30)
    year =models.IntegerField()
    price =models.DecimalField(max_digits=10,decimal_places=2)
    engine_type=models.CharField(max_length=20)
    transmission =models.CharField(max_length=20)
    mileage =models.DecimalField(max_digits=10,decimal_places=2)
    horse_power =models.DecimalField(max_digits=10,decimal_places=2)
    torque =models.DecimalField(max_digits=10,decimal_places=2)

# class Reviews(models.Model):
#     user_id =models.ForeignKey()


