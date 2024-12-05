from django.shortcuts import render, HttpResponse
import json
# from .models import Log
import aiml
import os
from django.conf import settings
from programy.clients.embed.basic import EmbeddedDataFileBot

#

BRAIN_FILE = os.path.join(settings.BASE_DIR, "pretrained_model/aiml_pretrained_model.dump")

k = aiml.Kernel()

if os.path.exists(BRAIN_FILE):
    print("Loading from brain file: " + BRAIN_FILE)
    k.loadBrain(BRAIN_FILE)
else:
    print("Parsing aiml files")
    k.bootstrap(learnFiles=os.path.join(settings.BASE_DIR, "pretrained_model/learningFileList.aiml"), commands="load aiml")
    print("Saving brain file: " + BRAIN_FILE)
    k.saveBrain(BRAIN_FILE)

#

filepath1 = os.path.join(settings.BASE_DIR, 'mybots1/storage/')


files1 = {'aiml': [filepath1 + 'categories'],
          'properties': filepath1 + 'properties/properties.txt'}

my_bot1 = EmbeddedDataFileBot(files1, defaults=True)


def home(request):
    return render(request, 'botapp/index.html')


def question(request):
    if request.method == "POST":
        query = json.loads(request.body)['input']

        answer = my_bot1.ask_question(query)

        if answer is None:
            answer = k.respond(query)

            # log = json.dumps({query: answer})
            # Log.objects.create(logs=log)

            return HttpResponse(answer)

        # log = json.dumps({query: answer})
        # Log.objects.create(logs=log)

        return HttpResponse(answer)
    else:
        return HttpResponse('Failed to get any question!')
