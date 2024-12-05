import json
import os
import sys
import cv2
import base64

from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.core.files.storage import FileSystemStorage
from requests import Response

sys.path.append(os.path.join(os.getcwd(), "all_functions/road_cracks"))
from all_functions.road_cracks.Detector import main
from all_functions.road_cracks.Detection_on_Video import video_cracks


def image_crack_detection(input_image):
    input_path = os.path.join(os.getcwd(), 'media', "upload.png")
    output_path = os.path.join(os.getcwd(), 'media', "prediction.png")
    os.remove(input_path) if os.path.exists(input_path) else None
    os.remove(output_path) if os.path.exists(output_path) else None

    fss = FileSystemStorage()
    file = fss.save("upload.png", input_image)

    img_abs_path = os.path.join(os.getcwd(), 'media', "upload.png")
    predicted_img, crack_counts = main(img_abs_path)

    # print(predicted_img)
    cv2.imwrite("media/prediction.png", predicted_img)
    file_url1 = fss.url("prediction.png")

    return {'file_url1': file_url1, 'status': True, 'count_cracks': crack_counts, 'type': 'image'}


def video_crack_detection(input_video):
    input_path = os.path.join(os.getcwd(), 'media', "upload.mp4")
    output_path = os.path.join(os.getcwd(), 'media', "prediction.mp4")
    os.remove(input_path) if os.path.exists(input_path) else None
    os.remove(output_path) if os.path.exists(output_path) else None

    fss = FileSystemStorage()
    file = fss.save("upload.mp4", input_video)

    video_abs_path = os.path.join(os.getcwd(), 'media', "upload.mp4")
    video_cracks(video_abs_path)

    return {'status': True, 'type': 'video'}


def home(request):
    return render(request, "index.html")


def detect(request):
    if request.method == "POST":
        input_file = request.FILES["myfile"]
        file_format = str(input_file).split(".")[-1].lower()

        accepted_image_types = ['jpg', 'jpeg', 'png']
        accepted_video_types = ['mp4', 'mkv']

        content = image_crack_detection(input_file) if file_format in accepted_image_types else video_crack_detection(input_file) if file_format in accepted_video_types else {
            'status': False}

        return render(request, 'detect.html', content)

    return render(request, "detect.html")
