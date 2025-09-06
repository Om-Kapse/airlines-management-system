from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_flights, name='search_flights'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('history/', views.booking_history, name='booking_history'),
    path('cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),  # 👈 new
]
