import re

from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import UserExtension
from .currency_conversion import get_initial_balance
from payapp.models import TransactionHistory


# Create your views here.
# home view
def home(request):
    if request.user.is_authenticated:

        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(status=TransactionHistory.pending)).count()

        return render(request, 'home.html', {'user': user_data, 'count': notifications_count})

    return render(request, 'register/SignIn.html')


# signup view
def signup(request):
    if request.method == "POST":
        f_name = request.POST['f-name']
        l_name = request.POST['l-name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        retype_password = request.POST['re_pass']
        currency = request.POST['currency']
        is_admin = request.POST.get('admin')

        # validate user data
        if User.objects.filter(username=username):
            messages.error(request, "Username already exists!")
            return redirect('register:signup')

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters")
            return redirect('register:signup')

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numeric")
            return redirect('register:signup')

        if User.objects.filter(email=email):
            messages.error(request, "Email already registered!")
            return redirect('register:signup')

        if password != retype_password:
            messages.error(request, "Passwords didn't matched")
            return redirect('register:signup')

        password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
        if re.match(password_pattern, password) is None:
            messages.error(request, "Password requirements failed")
            return redirect('register:signup')

        my_user = User.objects.create_user(username=username, email=email, password=password)
        if is_admin:
            my_user.is_superuser = True
        my_user.save()

        user = User.objects.get(username=username)
        balance = get_initial_balance(currency, 1000)
        UserExtension.objects.create(user=user, f_name=f_name, l_name=l_name, currency=currency, balance=balance)

        messages.success(request,
                         "Your Account has been created Successfully.")

        return redirect('register:signin')
    return render(request, 'register/SignUp.html')


# login view
def signin(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['pass']

        user = authenticate(username=name, password=password)

        if user is not None:
            login(request, user)
            return redirect('register:home')
        else:
            messages.error(request, "Bad Credentials")
            return redirect('register:signin')
    return render(request, 'register/SignIn.html')


# logout view
def signout(request):
    logout(request)
    return redirect('register:home')


def add_admin(request):
    if request.user.is_authenticated and request.user.is_superuser:
        if request.method == "POST":
            f_name = request.POST['f-name']
            l_name = request.POST['l-name']
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['pass']
            retype_password = request.POST['re_pass']
            currency = request.POST['currency']
            is_admin = request.POST.get('admin')

            # validate user data
            if User.objects.filter(username=username):
                messages.error(request, "Username already exists!")
                return redirect('register:register_admin')

            if len(username) > 15:
                messages.error(request, "Username must be under 15 characters")
                return redirect('register:register_admin')

            if not username.isalnum():
                messages.error(request, "Username must be Alpha-Numeric")
                return redirect('register:register_admin')

            if User.objects.filter(email=email):
                messages.error(request, "Email already registered!")
                return redirect('register:register_admin')

            if password != retype_password:
                messages.error(request, "Passwords didn't matched")
                return redirect('register:register_admin')

            password_pattern = "^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$"
            if re.match(password_pattern, password) is None:
                messages.error(request, "Password requirements failed")
                return redirect('register:register_admin')

            my_user = User.objects.create_user(username=username, email=email, password=password)
            if is_admin:
                my_user.is_superuser = True
            my_user.save()

            user = User.objects.get(username=username)
            balance = get_initial_balance(currency, 1000)
            UserExtension.objects.create(user=user, f_name=f_name, l_name=l_name, currency=currency, balance=balance)

            messages.success(request,
                             "Your Account has been created Successfully.")

            return redirect('register:home')

        user_data = UserExtension.objects.get(user=request.user)
        notifications_count = TransactionHistory.objects.filter(
            Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
                status=TransactionHistory.pending)).count()

        return render(request, 'register/registerAdmin.html', {'user': user_data, 'count': notifications_count})

    return render(request, 'register/SignUp.html')


def view_profile(request):
    user_data = UserExtension.objects.get(user=request.user)
    notifications_count = TransactionHistory.objects.filter(
        Q(mode=TransactionHistory.request) & Q(receiver=request.user) & Q(
            status=TransactionHistory.pending)).count()
    return render(request, 'register/profile.html', {'user': user_data, 'count': notifications_count})
