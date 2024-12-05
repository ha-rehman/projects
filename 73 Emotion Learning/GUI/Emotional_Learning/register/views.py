import re
from datetime import datetime

import cv2
import time
from django.db.models import Q
from django.http import StreamingHttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from utils.function import text_drawing, generate_session_id, predictor
from .models import EmotionHistory
from itertools import groupby


camera = None  # Declare the camera object at the module level


# Create your views here.
# home view
def home(request):
    if request.user.is_authenticated:
        return render(request, 'home_old.html')

    return render(request, 'register/SignIn.html')


def camera_stream(request):
    return StreamingHttpResponse(stream_camera(request), content_type="multipart/x-mixed-replace;boundary=frame")


def stream_camera(request):
    global camera
    detection_time_period = 10
    last_call_time = time.time()
    session_id = generate_session_id(request)
    camera = cv2.VideoCapture(0)  # Use the default camera (change the index if needed)
    label = None
    while True:

        success, frame = camera.read()
        if not success:
            break

        current_time = time.time()
        if current_time - last_call_time >= detection_time_period:
            label = predictor(frame)
            last_call_time = current_time
            last_call_time_formatted = datetime.now().time()

            EmotionHistory.objects.create(user_id=request.user, label=label, session_id=session_id)

        if label is not None:
            frame = text_drawing(frame, label, last_call_time_formatted)

        _, buffer = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')

    camera.release()


# stop camera stream
def stop_camera_stream(request):
    global camera
    if camera is not None:
        camera.release()  # Release the camera object
        camera = None  # Set the camera object to None
    return redirect('register:history')


def history(request):
    global camera
    if camera is not None:
        camera.release()  # Release the camera object
        camera = None  # Set the camera object to None

    records = EmotionHistory.objects.filter(user_id=request.user).order_by('session_id')

    # Group records by session ID
    grouped_records = {}
    for key, group in groupby(records, key=lambda x: x.session_id):
        grouped_records[key] = list(group)

    context = {'grouped_records': grouped_records}
    return render(request, "history.html", context)


def session_history(request, id):
    records = EmotionHistory.objects.filter(session_id=id)
    context = {'records': records}
    return render(request, "session_history.html", context)


# signup view
def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['pass']
        retype_password = request.POST['re_pass']

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
        my_user.save()

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