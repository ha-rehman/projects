import os
import pickle
from django.http import JsonResponse
from django.shortcuts import render
from all_functions.FishFarmingAPI import FishFarmingEvaluation

model_path = os.path.join(os.getcwd(), "all_functions/Dt.pickle")

def index(request):
    if request.method == "POST":
        temperature = request.POST['temperature']
        tubidity = request.POST['tubidity']
        oxygen = request.POST['oxygen']
        ph = request.POST['ph']
        amonia = request.POST['amonia']
        nitrate = request.POST['nitrate']
        length = request.POST['length']
        weight = request.POST['weight']

        ff = FishFarmingEvaluation(model_path)
        score = ff.predict(temperature, tubidity, oxygen, ph, amonia, nitrate, length, weight)

        return JsonResponse({'label': score}, status=200)

    return render(request, 'index.html')