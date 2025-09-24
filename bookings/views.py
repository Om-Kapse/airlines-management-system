from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from flights.models import Flight
from flights.models import Booking
from django.contrib import messages

@login_required
def search_flights(request):
    flights = []
    if request.method == "POST":
        source = request.POST.get("source")
        destination = request.POST.get("destination")
        flights = Flight.objects.filter(source__icontains=source, destination__icontains=destination)
    return render(request, "bookings/search_flights.html", {"flights": flights})

@login_required
def book_flight(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    capacity = flight.airplane.capacity
    booked_seats = list(flight.bookings.values_list('seat_no', flat=True))

    # Generate seat numbers (list of integers 1..capacity)
    seat_numbers = list(range(1, capacity + 1))

    if request.method == "POST":
        seat_no = request.POST.get("seat_no")
        if seat_no in booked_seats:
            return render(request, "bookings/book_flight.html", {
                "flight": flight,
                "seat_numbers": seat_numbers,
                "booked_seats": booked_seats,
                "error": f"Seat {seat_no} is already booked!"
            })

        Booking.objects.create(
            passenger=request.user,
            flight=flight,
            seat_no=seat_no
        )
        messages.success(request, f"✅ Seat {seat_no} booked successfully!")
        return redirect("booking_history")

    return render(request, "bookings/book_flight.html", {
        "flight": flight,
        "seat_numbers": seat_numbers,
        "booked_seats": booked_seats
    })




from django.contrib.auth.decorators import login_required

@login_required
def booking_history(request):
    bookings = Booking.objects.filter(passenger=request.user).select_related("flight")
    return render(request, "bookings/booking_history.html", {"bookings": bookings})

# @login_required
# def cancel_booking(request, booking_id):
#     booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
#     booking.status = "cancelled"
#     booking.save()
#     return redirect("booking_history")

@login_required
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, passenger=request.user)
    booking.delete()
    return redirect("booking_history")  # back to passenger’s booking history