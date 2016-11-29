# -*- coding: utf-8 -*-
# import rest framework services
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# import db models serializers
from mainapp.serializers.serializer import ParaSerializer

# import cropped serializers for docs page
from mainapp.serializers.docs_serializer import AuthorizationSerializer

# import needed app models
from mainapp.models.helpermodels import WorkingDay
from mainapp.models.faculty import Para

# import my own helper methods
from ..utils.custom_utils import *


class TodayScheduleView(views.APIView):
    """
    API that returns JSON with schedule for user.
    User can be either student or professor.
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        current_weekday = datetime.date.today().weekday()  # integer 0-monday .. 6-Sunday
        today = WorkingDay.objects.get(dayoftheweeknumber=current_weekday)
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )

            student_group = user.profilemodel.student_group

            classes_for_today = Para.objects.filter(
                para_group=student_group,
                para_day=today,
                week_type=weektype,
                semester=current_semester
            )
            result = dict()
            for i, para in enumerate(classes_for_today):
                result["para_%s" % i] = ParaSerializer(para).data
            response = create_response_scelet('success', 'schedule for today', result)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class WeeklyScheduleView(views.APIView):
    """
    API endpoint to get user schedule for current week
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = get_weektype(todaysdate)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = dict()
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            student_group = user.profilemodel.student_group

            for day in range(0, 5):
                classes = Para.objects.filter(
                    para_group=student_group,
                    para_day__dayoftheweeknumber=day,
                    week_type=weektype,
                    semester=current_semester
                )

                day_js = dict()
                for i, para in enumerate(classes):
                    day_js["para_%s" % i] = ParaSerializer(para).data

                result["%s" % days[day]] = day_js
            response = create_response_scelet('success', 'schedule for current week', result)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class NextWeeklyScheduleView(views.APIView):
    """
    API endpoint to get user schedule for next week
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request, format=None):
        user = request.user
        todaysdate = datetime.date.today()
        weektype = not get_weektype(todaysdate)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        result = dict()
        if user.is_active:
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            student_group = user.profilemodel.student_group

            for day in range(0, 5):
                classes = Para.objects.filter(
                    para_group=student_group,
                    para_day__dayoftheweeknumber=day,
                    week_type=weektype,
                    semester=current_semester,
                )

                day_js = dict()
                for i, para in enumerate(classes):
                    day_js["para_%s" % i] = ParaSerializer(para).data

                result["%s" % days[day]] = day_js
            response = create_response_scelet('success', 'schedule for next week', result)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)