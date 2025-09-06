from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Flight, Airplane

# ✅ Restrict to admin only
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "admin":
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper

# Dashboard
@login_required
@admin_required
def admin_flights_dashboard(request):
    flights = Flight.objects.all()
    airplanes = Airplane.objects.all()
    return render(request, "flights/admin_dashboard.html", {"flights": flights, "airplanes": airplanes})

# Add Airplane
@login_required
@admin_required
def add_airplane(request):
    if request.method == "POST":
        model_name = request.POST.get("model_name")
        capacity = request.POST.get("capacity")
        Airplane.objects.create(model_name=model_name, capacity=capacity)
        return redirect("admin_flights_dashboard")
    return render(request, "flights/add_airplane.html")

# Add Flight
@login_required
@admin_required
def add_flight(request):
    airplanes = Airplane.objects.all()
    if request.method == "POST":
        flight_no = request.POST.get("flight_no")
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        departure_time = request.POST.get("departure_time")
        arrival_time = request.POST.get("arrival_time")
        airplane_id = request.POST.get("airplane")
        airplane = get_object_or_404(Airplane, id=airplane_id)

        Flight.objects.create(
            flight_no=flight_no,
            source=source,
            destination=destination,
            departure_time=departure_time,
            arrival_time=arrival_time,
            airplane=airplane,
        )
        return redirect("admin_flights_dashboard")
    return render(request, "flights/add_flight.html", {"airplanes": airplanes})

# Edit Airplane
@login_required
@admin_required
def edit_airplane(request, airplane_id):
    airplane = get_object_or_404(Airplane, id=airplane_id)
    if request.method == "POST":
        airplane.model_name = request.POST.get("model_name")
        airplane.capacity = request.POST.get("capacity")
        airplane.save()
        return redirect("admin_flights_dashboard")
    return render(request, "flights/edit_airplane.html", {"airplane": airplane})

# Delete Airplane
@login_required
@admin_required
def delete_airplane(request, airplane_id):
    airplane = get_object_or_404(Airplane, id=airplane_id)
    airplane.delete()
    return redirect("admin_flights_dashboard")


# Edit Flight
@login_required
@admin_required
def edit_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    airplanes = Airplane.objects.all()
    if request.method == "POST":
        flight.flight_no = request.POST.get("flight_no")
        flight.source = request.POST.get("source")
        flight.destination = request.POST.get("destination")
        flight.departure_time = request.POST.get("departure_time")
        flight.arrival_time = request.POST.get("arrival_time")
        flight.airplane = get_object_or_404(Airplane, id=request.POST.get("airplane"))
        flight.save()
        return redirect("admin_flights_dashboard")
    return render(request, "flights/edit_flight.html", {"flight": flight, "airplanes": airplanes})

# Delete Flight
@login_required
@admin_required
def delete_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    flight.delete()
    return redirect("admin_flights_dashboard")


from django.utils.timezone import now
from .models import Flight, Booking

# ✅ Restrict to staff role
def staff_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or request.user.role != "staff":
            return redirect("home")
        return view_func(request, *args, **kwargs)
    return wrapper

# Staff Dashboard → list today’s flights
@login_required
@staff_required
def staff_dashboard(request):
    today_flights = Flight.objects.filter(departure_time__date=now().date())
    return render(request, "flights/staff_dashboard.html", {"flights": today_flights})

# View passengers for a flight
@login_required
@staff_required
def flight_passengers(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    bookings = Booking.objects.filter(flight=flight)
    return render(request, "flights/flight_passengers.html", {"flight": flight, "bookings": bookings})

# Mark passenger as checked-in
@login_required
@staff_required
def checkin_passenger(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    booking.checked_in = True
    booking.save()
    return redirect("flight_passengers", flight_id=booking.flight.id)

from django.db.models import Count, Sum
from django.utils.timezone import now

@login_required
@admin_required
def reports_dashboard(request):
    today = now().date()

    # Daily bookings
    daily_bookings = Booking.objects.filter(booking_date__date=today).count()

    # Revenue today
    revenue_today = Booking.objects.filter(booking_date__date=today).aggregate(
        total=Sum("flight__price")
    )["total"] or 0

    # Most popular routes (top 3)
    popular_routes = (
        Booking.objects.values("flight__source", "flight__destination")
        .annotate(total=Count("id"))
        .order_by("-total")[:3]
    )

    context = {
        "daily_bookings": daily_bookings,
        "revenue_today": revenue_today,
        "popular_routes": popular_routes,
    }
    return render(request, "flights/reports_dashboard.html", context)

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
    booking.delete()
    return redirect("booking_history")  # back to passenger’s booking history
