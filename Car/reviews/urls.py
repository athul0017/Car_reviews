from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage with featured & latest cars
     # Newest cars page
]
