import os
import sys
from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from COCO_detection.Detector import detect_img



def index(request):
    return render(request, 'index.html')


def get_result(request):
    if request.method == "POST":
        img = request.FILES['upload']

        base = settings.BASE_DIR
        file_storage_path = os.path.join(base, "static/images/upload.png")
        os.remove(file_storage_path) if os.path.exists(file_storage_path) else None
        fss = FileSystemStorage()
        file = fss.save("static/images/upload.png", img)
        items, count = detect_img(file_storage_path)
        print("Detection Completed!")
        # items = ['car', 'desk', 'bat']
        # count = 3

        return JsonResponse({'items': items, 'count': count}, status=200)
    else:
        return JsonResponse({"error": ""}, status=400)