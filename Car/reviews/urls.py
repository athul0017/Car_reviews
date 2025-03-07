from django.urls import path
from . import views
from .views import login_view, signup_view
from django.contrib.auth import views as auth_views  # auth views
from .views import compare_cars
from .views import contact_page  # Import contact function

urlpatterns = [
    path('', views.index, name='index'),  # Homepage with featured & latest cars
    path('login/', login_view, name='login'),  # login page 
    path('signup/', signup_view, name='signup'),  # signup page
    path('cars/', views.car_listing, name='car_listing'),
    path('cars/<int:car_id>/', views.car_details, name='car_details'),  # Car details page
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),  # Logout page
    path('profile/', views.profile, name='profile'),  # Profile view
    path('profile/edit/', views.edit_profile, name='edit_profile'),  # Edit Profile view
    path('contact/', contact_page, name='contact'),  # URL for Contact Us
    path('compare/', views.compare_cars, name='compare_cars'),
]    