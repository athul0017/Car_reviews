from django.shortcuts import render,redirect
from .models import Car
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth.models import User

# Create your views here.


def index(request):

    latest_cars = Car.objects.all().order_by('-created_at')[:3]  # Get 3 latest cars
    featured_cars = Car.objects.filter(featured=True)[:4]  # Get top 4 featured cars
    
     
    return render(request, 'index.html', {'latest_cars': latest_cars , 'featured_cars': featured_cars})


def login_view(request):   
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to a home page after login
            else:
                # Handle invalid login
                error_message = 'Invalid login credentials'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            error_message = 'Passwords do not match'
        elif len(password) > 8:
            error_message = 'Password not execed than 8 character'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('login')  # Redirect to the login page after signup

        return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')