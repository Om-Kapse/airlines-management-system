from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

@login_required
def home_view(request):
    user = request.user
    if user.role == "admin":
        return redirect("admin_dashboard")
    elif user.role == "staff":
        return redirect("staff_dashboard")
    else:  # passenger
        return redirect("passenger_dashboard")
