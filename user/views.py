from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.models import Group
from patients.registrationForm import PatientRegistrationForm
from user.emailAuth import EmailAuth
from doctor.models import DoctorProfile, PatientsList
from patients.models import PatientConnectionRequest
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from user.deco import unauthorizedUser


# Create your views here.
@unauthorizedUser
def UserLogin(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(f"pass : {password}")

        print(f"Login attempt - Email: {email}")
        print(f"Password provided: {'Yes' if password else 'No'}")

        if not email or not password:
            messages.error(request, "Please provide both email and password.")
            return render(request, "login.html")

        user = EmailAuth(email=email, password=password)
        print(f"EmailAuth result: {user}")

        if user is not None:
            print(f"Logging in user: {user.first_name} {user.last_name}")
            login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")

            if user.groups.filter(name="DOC").exists():
                print("User is in DOC group, redirecting to DOC_DASH")
                return redirect("DOC")
            elif user.groups.filter(name="PAT").exists():
                print("User is in PAT group, redirecting to PAT_DASH")
                return redirect("PAT")
        else:
            print("Authentication failed - user is None")
            messages.error(request, "Invalid email or password. Please try again.")

    return render(request, "auth/login.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect("login")

@unauthorizedUser
def regpat(request):
    if request.method == "POST":
        form = PatientRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name="PAT")
            user.groups.add(group)
            login(request, user)  # Log the user in after registration
            return redirect("PAT")  # Change "home" to your desired redirect page
    else:
        form = PatientRegistrationForm()
    return render(request, "auth/register.html", {"form": form})
