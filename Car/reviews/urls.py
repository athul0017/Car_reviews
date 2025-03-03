from django.urls import path
from . import views 
from .views import login_view,signup_view

urlpatterns = [
    path('', views.index, name='index'),  # Homepage with featured & latest cars
     # Newest cars page
      path('login/', login_view, name='login'),#login page 
      path('signup/', signup_view, name='signup'),#signup page
]
