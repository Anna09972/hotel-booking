from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/add-room/', views.add_room, name='add_room'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('rooms/', views.room_list, name='rooms'),
    path('rooms/book/<int:room_id>/', views.booking_details, name='booking_details'),
    path('rooms/confirm/<int:room_id>/', views.confirm_booking, name='confirm_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
]
