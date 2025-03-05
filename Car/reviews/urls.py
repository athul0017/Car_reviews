from django.urls import path
from . import views 
from .views import login_view,signup_view
from django.contrib.auth import views as auth_views #auth views

urlpatterns = [
    path('', views.index, name='index'),  # Homepage with featured & latest cars
     # Newest cars page
    path('login/', login_view, name='login'),#login page 
    path('signup/', signup_view, name='signup'),#signup page
    path('cars/', views.car_listing, name='car_listing'), 
    path('cars/<int:car_id>/', views.car_details, name='car_details'),  # Car details page
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout page
]
