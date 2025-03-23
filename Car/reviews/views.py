from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode
from django.urls import reverse
from django.db.models import Avg  # ✅ Import Avg for calculating average rating
from .models import Car, Brand, Review
from .forms import LoginForm

def index(request):
    latest_cars = Car.objects.all().order_by('-created_at')[:3]  # Get 3 newest cars
    featured_cars = Car.objects.filter(featured=True)[:4]  # Get top 4 featured cars
    return render(request, 'index.html', {'latest_cars': latest_cars, 'featured_cars': featured_cars})

def contact_page(request):
    return render(request, 'contact.html')  # Show contact.html page

def compare_cars(request):
    from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Car

def compare_cars(request):
    if request.method == 'GET':
        selected_car_ids = request.GET.getlist('compare')

        # Check if exactly 2 cars are selected
        if len(selected_car_ids) != 2:
            # messages.error(request, "Please select exactly 2 cars to compare.")
            return redirect('car_listing')  # Redirect back to the car listing page
        
        # Validate car IDs (check if they exist in the database)
        try:
            selected_car_ids = [int(id) for id in selected_car_ids]  # Convert to integers
        except ValueError:
            messages.error(request, "Invalid car selection.")
            return redirect('car_listing')
        
        # Retrieve the cars to compare
        cars_to_compare = Car.objects.filter(id__in=selected_car_ids)
        
        # Ensure that exactly 2 cars are returned
        if cars_to_compare.count() != 2:
            messages.error(request, "Invalid car selection or cars not found.")
            return redirect('car_listing')
        
        # Additional check: Ensure that the selected cars are not the same
        if cars_to_compare[0].id == cars_to_compare[1].id:
            messages.error(request, "You cannot compare the same car with itself.")
            return redirect('car_listing')
        
        return render(request, 'compare_cars.html', {'car1': cars_to_compare[0], 'car2': cars_to_compare[1]})
    
    return redirect('car_listing')

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)

    # Allow deletion only if the user is the review owner or an admin
    if request.user == review.user or request.user.is_staff:
        review.delete()
        messages.success(request, "Your review has been deleted successfully.")
    else:
        messages.error(request, "You are not authorized to delete this review.")

    return redirect('car_details', car_id=review.car.id)  # Redirect to car details page



def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # If already logged in, go to homepage
    
    next_url = request.GET.get('next', 'index')  
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                return render(request, 'login.html', {'form': form, 'error_message': 'Invalid credentials'})
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form, 'next': next_url})

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')  # If already logged in, go to homepage

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error_message': 'Username already taken'})
        elif User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': 'Email already registered'})
        elif password != confirm_password:
            return render(request, 'signup.html', {'error_message': 'Passwords do not match'})
        elif len(password) < 8:
            return render(request, 'signup.html', {'error_message': 'Password must be at least 8 characters long'})
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')

    return render(request, 'signup.html')

def car_listing(request):
    cars = Car.objects.all().order_by('-created_at')
    brands = Brand.objects.all()

    # Get filters from request
    brand_filter = request.GET.get('brand', '').strip()
    category_filter = request.GET.get('category', '').strip()
    fuel_filter = request.GET.get('fuel', '').strip()
    price_filter = request.GET.get('price', '').strip()
    search_query = request.GET.get('search', '').strip()

    # Debugging Filters
    print(f"Filters -> Brand: {brand_filter}, Category: {category_filter}, Fuel: {fuel_filter}, Price: {price_filter}, Search: {search_query}")

    # Apply filters
    if brand_filter:
        cars = cars.filter(car_model__brand__bname__icontains=brand_filter)
    if category_filter:
        cars = cars.filter(category__icontains=category_filter)
    if fuel_filter:
        cars = cars.filter(engine_type__icontains=fuel_filter)
    if search_query:
        cars = cars.filter(car_model__model_name__icontains=search_query)
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

from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.urls import reverse
from django.utils.http import urlencode
from .models import Car, Review,CarGallery

def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car).order_by('-created_at')
    images = CarGallery.objects.filter(car=car)  # ✅ Fetch images for the car

    # Calculate the average rating
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    avg_rating = round(avg_rating, 1) if avg_rating else 0  # Round to 1 decimal place

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
            login_url = f"{reverse('login')}?{urlencode({'next': request.path})}"
            return redirect(login_url)

    # ✅ Pass `images` to the template
    return render(request, 'car_details.html', {
        'car': car,
        'reviews': reviews,
        'avg_rating': avg_rating,
        'images': images  # ✅ Added this line
    })


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username = request.POST.get('username', user.username).strip()
        email = request.POST.get('email', user.email).strip()

        # Check if new username/email is already taken
        if User.objects.exclude(id=user.id).filter(username=username).exists():
            return render(request, 'edit_profile.html', {'error_message': 'Username already taken'})
        if User.objects.exclude(id=user.id).filter(email=email).exists():
            return render(request, 'edit_profile.html', {'error_message': 'Email already registered'})

        # Update user details
        user.username = username
        user.email = email
        user.save()
        return redirect('profile')

    return render(request, 'edit_profile.html')

