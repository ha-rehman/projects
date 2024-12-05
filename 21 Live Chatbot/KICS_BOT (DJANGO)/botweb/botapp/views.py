from django.shortcuts import render, HttpResponse
import json
from .models import Log
import os
from programy.clients.embed.datafile import EmbeddedDataFileBot
from programy.clients.args import CommandLineClientArguments
from django.conf import settings



# Create your views here.


class EmbeddedBasicBot(EmbeddedDataFileBot):

    def __init__(self, logging_filename=None):
        # filepath = os.path.dirname(__file__) + os.sep
        # filepath = './program-y-master/src/programy/clients/embed/'
        filepath = os.path.join(settings.BASE_DIR, 'program-y-master/src/programy/clients/embed/')
        if logging_filename is not None:
            self._logging_filename = logging_filename
        else:
            self._logging_filename = filepath + 'basicbot/logging.yaml'

        files = {'aiml': [filepath + 'basicbot/categories'],
                 'learnf': [filepath + 'basicbot/learnf'],
                 'patterns': filepath + 'basicbot/nodes/pattern_nodes.conf',
                 'templates': filepath + 'basicbot/nodes/template_nodes.conf',
                 'properties': filepath + 'basicbot/properties/properties.txt',
                 'defaults': filepath + 'basicbot/properties/defaults.txt',
                 'sets': [filepath + 'basicbot/sets'],
                 'maps': [filepath + 'basicbot/maps'],
                 'rdfs': [filepath + 'basicbot/rdfs'],
                 'denormals': filepath + 'basicbot/lookups/denormal.txt',
                 'normals': filepath + 'basicbot/lookups/normal.txt',
                 'genders': filepath + 'basicbot/lookups/gender.txt',
                 'persons': filepath + 'basicbot/lookups/person.txt',
                 'person2s': filepath + 'basicbot/lookups/person2.txt',
                 'regexes': filepath + 'basicbot/regex/regex-templates.txt',
                 'spellings': filepath + 'basicbot/spelling/corpus.txt',
                 'preprocessors': filepath + 'basicbot/processing/preprocessors.conf',
                 'postprocessors': filepath + 'basicbot/processing/postprocessors.conf',
                 'postquestionprocessors': filepath + 'basicbot/processing/postquestionprocessors.conf'
                 }
        EmbeddedDataFileBot.__init__(self, files)

    def parse_arguments(self, argument_parser):
        client_args = CommandLineClientArguments(self, parser=None)
        if self._logging_filename is not None:
            client_args._logging = self._logging_filename
        return client_args


if __name__ == '__main__':

    print("Loading Bot Brain....please wait!")





def home(request):
    return render(request, 'botapp/index.html')


def question(request):
    if request.method == "POST":
        my_bot = EmbeddedBasicBot()
        query = json.loads(request.body)['input']
        answer = my_bot.ask_question(query)

        log = json.dumps({query: answer})
        Log.objects.create(logs=log)



        return HttpResponse(answer)


