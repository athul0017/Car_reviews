from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode
from django.urls import reverse
from .models import Car, Brand, Review
from .forms import LoginForm

def index(request):
    latest_cars = Car.objects.all().order_by('-created_at')[:3]  # Get 3 latest cars
    featured_cars = Car.objects.filter(featured=True)[:4]  # Get top 4 featured cars
    return render(request, 'index.html', {'latest_cars': latest_cars, 'featured_cars': featured_cars})

def login_view(request):   
    next_url = request.GET.get('next', 'index')  # Get 'next' parameter if available
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)  # Redirect to 'next' URL after login
            else:
                error_message = 'Invalid login credentials'
                return render(request, 'login.html', {'form': form, 'error_message': error_message})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form, 'next': next_url})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if User.objects.filter(username=username).exists():
            error_message = 'Username already taken'
        elif password != confirm_password:
            error_message = 'Passwords do not match'
        elif len(password) < 8:
            error_message = 'Password should be at least 8 characters long'
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('index')  # Redirect to homepage after signup

        return render(request, 'signup.html', {'error_message': error_message})

    return render(request, 'signup.html')

def car_listing(request):
    cars = Car.objects.all().order_by('-created_at')
    brands = Brand.objects.all()
    
    # Get filters from request
    brand_filter = request.GET.get('brand', '')
    category_filter = request.GET.get('category', '')
    fuel_filter = request.GET.get('fuel', '')
    price_filter = request.GET.get('price', '')
    search_query = request.GET.get('search', '')

    print("Filters Applied:")  # Debugging
    print(f"Brand: {brand_filter}, Category: {category_filter}, Fuel: {fuel_filter}, Price: {price_filter}, Search: {search_query}")

    # Apply filters
    if brand_filter:
        cars = cars.filter(car_model__brand__bname__icontains=brand_filter)
    if category_filter:
        cars = cars.filter(category__icontains=category_filter)
    if fuel_filter:
        cars = cars.filter(engine_type__icontains=fuel_filter)
    if search_query:
        cars = cars.filter(car_model__model_name__icontains=search_query)

    # Price filtering
    if price_filter and '-' in price_filter:
        try:
            min_price, max_price = price_filter.split('-')
            min_price = int(min_price) * 100000  # Convert Lakhs to Rupees
            max_price = int(max_price.replace('L', '')) * 100000  # Convert Lakhs to Rupees
            cars = cars.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            print("Invalid price range format")  # Debugging

    # Pagination (6 cars per page)
    paginator = Paginator(cars, 6)
    page_number = request.GET.get('page')
    cars_page = paginator.get_page(page_number)

    return render(request, 'car_listing.html', {'cars': cars_page, 'brands': brands})

def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car)

    if request.method == "POST":
        if request.user.is_authenticated:
            review_rating = request.POST.get("review_rating")
            review_text = request.POST.get("review_text")

            if review_rating and review_text:
                Review.objects.create(
                    car=car,
                    user=request.user,
                    rating=int(review_rating),
                    review_text=review_text
                )
                return redirect('car_details', car_id=car.id)
        else:
            # Redirect to login with a 'next' parameter to return to this page after login
            login_url = f"{reverse('login')}?{urlencode({'next': request.path})}"
            return redirect(login_url)

    return render(request, 'car_details.html', {'car': car, 'reviews': reviews})
