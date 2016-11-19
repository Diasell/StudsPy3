import requests
#  import django services
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

# import rest framework services
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication)
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


# import db models serializers
from mainapp.serializers.serializer import (
    UserSerializer,
    ProfileSerializer,
    ParaSerializer,
    StudentJournalSerializer)

# import cropped serializers for docs page
from mainapp.serializers.docs_serializer import (
    RegisterViewSerializer,
    LoginViewSerializer,
    AuthorizationSerializer,
    GroupStudentsSerializer,
    GetStJournalSerializer)

# import needed app models
from mainapp.models.userProfile import ProfileModel
from mainapp.models.student import StudentJournalModel
from mainapp.models.helpermodels import WorkingDay
from mainapp.models.faculty import (
    Para,
    ParaTime,
    Disciplines,
    StudentGroupModel,
    FacultyModel,
    DepartmentModel)

# import my own helper methods
from ..utils.custom_utils import *

import json, requests

TELEGRAM = 'https://api.telegram.org/bot289647729:AAENTWQjxU_JMOxnaEqffkwKqjhwV3NWHmU/sendMessage'

def get_schedule(chat_id):
    profile = ProfileModel.objects.get(chat_id=chat_id)
    todaysdate = datetime.date.today()
    weektype = get_weektype(todaysdate)
    current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
    today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)
    current_semester = StartSemester.objects.get(
        semesterstart__lt=todaysdate,
        semesterend__gt=todaysdate
    )
    if profile.is_student:
        student_group = profile.student_group

        classes_for_today = Para.objects.filter(
            para_group=student_group,
            para_day=today,
            week_type=weektype,
            semester=current_semester
        )
        result = ''
        for i, para in enumerate(classes_for_today):
            result += ParaSerializer(para).data['para_number'] + ' : ' + ParaSerializer(para).data['discipline'] + "\n"
        a = {}
        a["chat_id"] = chat_id
        a['text'] = result
        return a


def help(chat_id):
    a = {}
    a["chat_id"] = chat_id
    a['text'] = "commands:\n/schedule" + '\n' + 'chat_id: ' + str(chat_id)
    return a
class TelegramBotView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        data = request.data

        commands = {
            u'/старт': help,
            'команди': help,
            '/розклад': get_schedule,
        }

        chat_id = data['message']['chat']['id']
        user_command = data['message']['text']

        func = commands.get(user_command.lower())
        print(func)
        if func:
            req = requests.post(TELEGRAM, func(chat_id))
        else:
            req = requests.post(TELEGRAM, help(chat_id))

        return Response(req.json(), status=req.status_code)