from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.utils.http import urlencode
from django.urls import reverse
from django.db.models import Avg
from .models import Car, Brand, Review, CarGallery, MileageReport
from .forms import LoginForm, MileageReportForm


def index(request):
    latest_cars = Car.objects.all().order_by('-created_at')[:3]  # Get 3 newest cars
    featured_cars = Car.objects.filter(featured=True)[:4]  # Get top 4 featured cars
    return render(request, 'index.html', {'latest_cars': latest_cars, 'featured_cars': featured_cars})


@login_required(login_url='/login/')  # Redirects to login page if user not logged in
def contact_page(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # For now — just display a thank you message
        return HttpResponse(f"Thank you {name}! We have received your message.")

    return render(request, 'contact.html')


def compare_cars(request):
    selected_car_ids = request.GET.getlist('compare')

    if len(selected_car_ids) != 2:
        messages.error(request, "Please select exactly two cars to compare.")
        return redirect('car_listing')

    try:
        selected_car_ids = [int(id) for id in selected_car_ids]
    except ValueError:
        messages.error(request, "Invalid car selection.")
        return redirect('car_listing')

    cars_to_compare = Car.objects.filter(id__in=selected_car_ids)

    if cars_to_compare.count() != 2 or cars_to_compare[0].id == cars_to_compare[1].id:
        messages.error(request, "Invalid car selection. Please select two different cars.")
        return redirect('car_listing')

    return render(request, 'compare_cars.html', {'car1': cars_to_compare[0], 'car2': cars_to_compare[1]})


@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.user == review.user:  # Ensure user can only delete their own review
        review.delete()
        messages.get_messages(request)  # Clears previous messages
        messages.success(request, "Your review has been deleted successfully.")
    return redirect('car_details', car_id=review.car.id)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    next_url = request.GET.get('next', 'index')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user:
                login(request, user)
                return redirect(next_url)
            messages.error(request, 'Invalid credentials')

    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form, 'next': next_url})


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered')
        elif password != confirm_password:
            messages.error(request, 'Passwords do not match')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user)
            return redirect('index')

    return render(request, 'signup.html')


def car_listing(request):
    cars = Car.objects.all().order_by('-created_at')
    brands = Brand.objects.all()

    brand_filter = request.GET.get('brand', '').strip()
    category_filter = request.GET.get('category', '').strip()
    fuel_filter = request.GET.get('fuel', '').strip()
    price_filter = request.GET.get('price', '').strip()
    search_query = request.GET.get('search', '').strip()

    if brand_filter:
        cars = cars.filter(car_model__brand__bname__icontains=brand_filter)
    if category_filter:
        cars = cars.filter(category__icontains=category_filter)
    if fuel_filter:
        cars = cars.filter(engine_type__icontains=fuel_filter)
    if search_query:
        cars = cars.filter(car_model__model_name__icontains=search_query)

    if price_filter and '-' in price_filter:
        try:
            min_price, max_price = price_filter.split('-')
            min_price, max_price = int(min_price) * 100000, int(max_price.replace('L', '')) * 100000
            cars = cars.filter(price__gte=min_price, price__lte=max_price)
        except ValueError:
            pass

    paginator = Paginator(cars, 6)
    cars_page = paginator.get_page(request.GET.get('page'))

    return render(request, 'car_listing.html', {'cars': cars_page, 'brands': brands})


from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.db.models import Avg
from urllib.parse import urlencode
from .models import Car, Review, CarGallery, MileageReport
from .forms import MileageReportForm
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Avg
from django.contrib.auth.decorators import login_required
from urllib.parse import urlencode
from django.urls import reverse
from .models import Car, Review, CarGallery, MileageReport
from .forms import MileageReportForm

def car_details(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    reviews = Review.objects.filter(car=car).order_by('-created_at')
    images = CarGallery.objects.filter(car=car)
    mileage_reports = MileageReport.objects.filter(car=car)

    avg_rating = round(reviews.aggregate(Avg('rating'))['rating__avg'] or 0, 1)
    avg_mileage = round(mileage_reports.aggregate(Avg('mileage'))['mileage__avg'] or 0, 2) if mileage_reports else "Not reported yet"

    mileage_form = MileageReportForm()

    if request.method == "POST":
        print("POST Data:", request.POST)  # Debugging statement

        if request.user.is_authenticated:
            if 'review_submit' in request.POST:
                review_rating = request.POST.get("review_rating")
                review_text = request.POST.get("review_text")

                if review_rating and review_text:
                    new_review = Review.objects.create(
                        car=car, user=request.user, rating=int(review_rating), review_text=review_text
                    )
                    print("Review Saved:", new_review)  # Debugging statement
                    return redirect('car_details', car_id=car.id)

            elif 'mileage_submit' in request.POST:
                mileage_form = MileageReportForm(request.POST)
                if mileage_form.is_valid():
                    mileage_report = mileage_form.save(commit=False)
                    mileage_report.car = car
                    mileage_report.user = request.user
                    mileage_report.save()
                    print("Mileage Saved:", mileage_report)  # Debugging statement
                    return redirect('car_details', car_id=car.id)

        else:
            return redirect(f"{reverse('login')}?{urlencode({'next': request.path})}")

    return render(request, 'car_details.html', {
        'car': car, 'reviews': reviews, 'avg_rating': avg_rating,
        'images': images, 'mileage_reports': mileage_reports,
        'avg_mileage': avg_mileage, 'mileage_form': mileage_form,
    })



@login_required
def submit_mileage(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    form = MileageReportForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        mileage_report = form.save(commit=False)
        mileage_report.car, mileage_report.user = car, request.user
        mileage_report.save()
        return redirect('car_details', car_id=car.id)

    return render(request, 'submit_mileage.html', {'form': form, 'car': car})


@login_required
def profile(request):
    return render(request, 'profile.html', {'user': request.user})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        username, email = request.POST.get('username', user.username).strip(), request.POST.get('email', user.email).strip()

        if User.objects.exclude(id=user.id).filter(username=username).exists():
            messages.error(request, 'Username already taken')
        elif User.objects.exclude(id=user.id).filter(email=email).exists():
            messages.error(request, 'Email already registered')
        else:
            user.username, user.email = username, email
            user.save()
            return redirect('profile')

    return render(request, 'edit_profile.html')

