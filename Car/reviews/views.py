from django.shortcuts import render
from .models import Car

# Create your views here.


def index(request):

    latest_cars = Car.objects.all().order_by('-created_at')[:3]  # Get 3 latest cars
    featured_cars = Car.objects.filter(featured=True)[:4]  # Get top 4 featured cars
    
     
    return render(request, 'index.html', {'latest_cars': latest_cars , 'featured_cars': featured_cars})


