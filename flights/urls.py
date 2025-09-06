from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_flights_dashboard, name='admin_flights_dashboard'),

    # Airplanes
    path('add-airplane/', views.add_airplane, name='add_airplane'),
    path('edit-airplane/<int:airplane_id>/', views.edit_airplane, name='edit_airplane'),
    path('delete-airplane/<int:airplane_id>/', views.delete_airplane, name='delete_airplane'),

    # Flights
    path('add-flight/', views.add_flight, name='add_flight'),
    path('edit-flight/<int:flight_id>/', views.edit_flight, name='edit_flight'),
    path('delete-flight/<int:flight_id>/', views.delete_flight, name='delete_flight'),
]
urlpatterns += [
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/flight/<int:flight_id>/', views.flight_passengers, name='flight_passengers'),
    path('staff/checkin/<int:booking_id>/', views.checkin_passenger, name='checkin_passenger'),
]
urlpatterns += [
    path('admin/reports/', views.reports_dashboard, name='reports_dashboard'),
]
urlpatterns += [
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
]
