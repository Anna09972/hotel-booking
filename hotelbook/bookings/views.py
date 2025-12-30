from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Room, Booking, Hotel
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout


def index(request):
    return render(request, 'index.html')


def is_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    rooms = Room.objects.all()
    bookings = Booking.objects.select_related('room', 'user')
    return render(request, 'admin_dashboard.html', {
        'rooms': rooms,
        'bookings': bookings
    })

@login_required
@user_passes_test(is_admin)
def add_room(request):
    hotels = Hotel.objects.all()

    if request.method == "POST":

        # 🔹 ADD HOTEL FORM
        if 'add_hotel' in request.POST:
            Hotel.objects.create(
                name=request.POST.get('hotel_name'),
                location=request.POST.get('hotel_location'),
                description=request.POST.get('hotel_description'),
                contact_number=request.POST.get('hotel_contact'),
                email=request.POST.get('hotel_email'),
            )
            return redirect('add_room')  # refresh page to update dropdown

        # 🔹 ADD ROOM FORM
        if 'add_room' in request.POST:
            Room.objects.create(
                hotel_id=request.POST.get('hotel'),
                room_number=request.POST.get('room_number'),
                room_type=request.POST.get('room_type'),
                price_per_night=request.POST.get('price'),
                is_available=True
            )
            return redirect('admin_dashboard')

    return render(request, 'admin_add_room.html', {
        'hotels': hotels
    })

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('rooms')
        else:
            messages.error(request, "Invalid username or password")

    return render(request, 'login.html')


def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['confirm']

        if password != confirm:
            messages.error(request, "Passwords do not match")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('login')

    return render(request, 'register.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'rooms.html', {
        'rooms': rooms
    })


@login_required
def booking_details(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    return render(request, 'booking_details.html', {
        'room': room,
        'hotel': room.hotel
    })


@login_required
def confirm_booking(request, room_id):
    room = get_object_or_404(Room, id=room_id, is_available=True)

    if request.method == "POST":
        Booking.objects.create(
            user=request.user,
            room=room,
            check_in=None,    
            check_out=None
        )

        room.is_available = False
        room.save()

        messages.success(request, "Booking confirmed successfully!")
        return redirect('my_bookings')

    return redirect('rooms')

@login_required
def my_bookings(request):
    bookings = Booking.objects.filter(user=request.user).select_related('room', 'room__hotel')
    return render(request, 'my_bookings.html', {
        'bookings': bookings
    })
