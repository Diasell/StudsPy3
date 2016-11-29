# -*- coding: utf-8 -*-
from django.contrib.auth.models import User

# import rest framework services
from rest_framework.authentication import TokenAuthentication
from rest_framework import status, views
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


# import db models serializers
from mainapp.serializers.serializer import (
    ProfileSerializer,
    StudentJournalSerializer)

# import cropped serializers for docs page
from mainapp.serializers.docs_serializer import (
    AuthorizationSerializer,
    GetStJournalSerializer)

# import needed app models
from mainapp.models.userProfile import ProfileModel
from mainapp.models.student import StudentJournalModel
from mainapp.models.faculty import (
    Para,
    ParaTime,
    Disciplines,
    StudentGroupModel,
    FacultyModel,
    DepartmentModel)

# import my own helper methods
from ..utils.custom_utils import *


class GroupStudentListView(views.APIView):
    """
    API endpoint to show all the students for the given group
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            requested_group = user.profilemodel.student_group
            list_of_students = ProfileModel.objects.filter(
                student_group=requested_group
            )

            result = []
            for student in list_of_students:
                stud_dict = dict()
                temp = ProfileSerializer(student).data
                for key in temp:
                    stud_dict[key] = temp[key]
                result.append(stud_dict)

            response = create_response_scelet('success', 'List of classmates', result)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ListOfDisciplinesView(APIView):
    """
    API endpoint that allows student user to check
    what classes he/she has during current semester
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()

            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            student_group = user.profilemodel.student_group

            disciplines = Para.objects.filter(
                semester=current_semester,
                para_group=student_group
            ).values_list('para_subject__discipline', flat=True).distinct()
            items = list(disciplines)
            items = sorted(items)
            response = []

            for discipline in items:
                result = dict()
                result['para'] = discipline
                para = Para.objects.filter(
                    semester=current_semester,
                    para_group=student_group,
                    para_subject__discipline=discipline
                )[0]
                result['professor'] = para.para_professor.user.get_full_name()
                result['room'] = para.para_professor.room
                try:
                    result['photo'] = para.para_professor.photo.url
                except ValueError:
                    result['photo'] = ''
                response.append(result)
            data = create_response_scelet('success', 'List of disciplines for current semester', response)
            return Response(data, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ListFacultyView(APIView):
    permission_classes = (AllowAny, )

    def get(self, request):
        response = dict()
        fac_list = FacultyModel.objects.all()
        for faculty in fac_list:
            groups = []
            dep_list = DepartmentModel.objects.filter(
                faculty=faculty
            )
            for department in dep_list:
                groups_list = StudentGroupModel.objects.filter(
                    department=department
                )
                for group in groups_list:
                    groups.append([group.title,
                                   group.date_started,
                                   group_year(group.date_started)])
            response[faculty.title] = groups
        data = create_response_scelet('success', 'Faculties structure', response)
        return Response(data, status=status.HTTP_200_OK)



#  All code below is not used anywhere


class GroupsListView(APIView):
    """
    API endpoint that allows professor user to get
    the list of all the group that he is currently
    teaching(current Semester)
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AuthorizationSerializer

    def get(self, request):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()
            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            groups = Para.objects.filter(
                semester=current_semester,
                para_professor=user.profilemodel
            ).values_list('para_group__title', flat=True).distinct()
            result = dict()
            for number, group in enumerate(groups):
                result[number+1] = group
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"Authorization": "This is not an active user"},
                            status=status.HTTP_401_UNAUTHORIZED)


class StudentJournalInstanceView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = StudentJournalSerializer

    def post(self, request, *args, **kwargs):
        """
        Method to save StudentJournalModel instance for Professors users
        """
        user = request.user
        has_perm = user.has_perm('mainapp.add_studentjournalmodel')
        if user.is_active:
            if has_perm:
                value = self.request.data['value']
                date = self.request.data['date']
                discipline = self.request.data['discipline']
                para_number = self.request.data['para_number']
                student = self.request.data['student']
                is_module = self.request.data['is_module']

                try:
                    new_instance = StudentJournalModel.objects.create(
                        value=value,
                        date=date,
                        discipline=Disciplines.objects.get(discipline=discipline),
                        para_number=ParaTime.objects.get(para_position=para_number),
                        student=User.objects.get(username=student),
                        is_module=is_module
                    )
                except Exception:
                    return Response({"Failed": "Not valid data"},
                                    status=status.HTTP_403_FORBIDDEN)
                new_instance.save()
                serialized = StudentJournalSerializer(new_instance)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            return Response({"Permissions": "User has not enough permissions"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"Authorization": "This is not an active user"},
                        status=status.HTTP_401_UNAUTHORIZED)

    def put(self, request, *args, **kwargs):
        """
        Method that allows professor user to edit the StudentJournalModel instance
        """
        user = request.user
        has_perm = user.has_perm('mainapp.change_studentjournalmodel')
        if user.is_active:
            if has_perm:
                pk = self.request.data['pk']
                value = self.request.data['value']
                date = self.request.data['date']
                discipline = self.request.data['discipline']
                para_number = self.request.data['para_number']
                student = self.request.data['student']
                is_module = self.request.data['is_module']

                edit_obj = StudentJournalModel.objects.get(pk=pk)
                try:
                    edit_obj.value = value
                    edit_obj.date = date
                    edit_obj.discipline = Disciplines.objects.get(discipline=discipline)
                    edit_obj.para_number = ParaTime.objects.get(para_position=para_number)
                    edit_obj.student = User.objects.get(username=student)
                    edit_obj.is_module = is_module
                except Exception:
                    return Response({"Failed": "Not valid data"},
                                    status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
                edit_obj.save()
                serialized = StudentJournalSerializer(edit_obj)
                return Response(serialized.data, status=status.HTTP_201_CREATED)
            return Response({"Permissions": "User has not enough permissions"},
                            status=status.HTTP_403_FORBIDDEN)
        return Response({"Authorization": "This is not an active user"},
                        status=status.HTTP_401_UNAUTHORIZED)


class StudentClassJournalView(views.APIView):
    """
    API endpoint that allows user to get students results for given
    student, discipline, range(default range is whole current semester)
    """

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, )
    serializer_class = GetStJournalSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        if user.is_active:
            todaysdate = datetime.date.today()

            current_semester = StartSemester.objects.get(
                semesterstart__lt=todaysdate,
                semesterend__gt=todaysdate
            )
            try:
                start_date = self.request.data['start_date']
            except Exception:
                start_date = current_semester.semesterstart
            try:
                end_date = self.request.data['end_date']
            except Exception:
                end_date = current_semester.semesterend

            discipline = self.request.data['discipline']

            journal = StudentJournalModel.objects.filter(
                student=user,
                discipline=Disciplines.objects.get(discipline=discipline),
                date__range=[start_date, end_date]
            )
            result = dict()
            total_value = 0
            missed_classes = 0
            for number, item in enumerate(journal):
                serialized_item = StudentJournalSerializer(item).data
                result[number+1] = serialized_item
                try:
                    total_value += int(serialized_item['value'])
                except Exception:
                    missed_classes += 1
            statistics = dict()
            statistics["total_value"] = total_value
            statistics["missed_classes"] = missed_classes
            statistics["number_of_classes"] = len(journal)

            result['stats'] = statistics

            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({"UnAuth": "Current user is not active"},
                            status=status.HTTP_401_UNAUTHORIZED)

