from django.db import models
from django.conf import settings

# Create your models here.
class Airplane(models.Model):
    model_name = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.model_name} (Capacity: {self.capacity})"

class Flight(models.Model):
    flight_no = models.CharField(max_length=20, unique=True)
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=100.00)  # ✅ ticket price

    def __str__(self):
        return f"{self.flight_no} - {self.source} → {self.destination}"

class Booking(models.Model):
    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="bookings")
    booking_date = models.DateTimeField(auto_now_add=True)
    checked_in = models.BooleanField(default=False)  # ✅ NEW
    seat_no = models.CharField(max_length=5,)  # ✅ add this


    def __str__(self):
        return f"{self.passenger.username} booked {self.flight.flight_no} (Seat {self.seat_no or 'TBD'})"
    # def __str__(self):
    #     return f"{self.passenger.username} booked {self.flight.flight_no}"

