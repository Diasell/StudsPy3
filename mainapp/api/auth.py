# -*- coding: utf-8 -*-
#  import django services
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError

# import rest framework services
from rest_framework.authtoken.models import Token
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView


# import db models serializers
from mainapp.serializers.serializer import (
    UserSerializer,
    ProfileSerializer)

# import cropped serializers for docs page
from mainapp.serializers.docs_serializer import (
    RegisterViewSerializer,
    LoginViewSerializer,
    EditProfileViewSerializer,
    AddChatIDSerializer,
    ChangePasswordSerializer,)

# import needed app models
from mainapp.models.userProfile import ProfileModel
from mainapp.models.faculty import (
    StudentGroupModel,
    FacultyModel)

# import my own helper methods
from ..utils.custom_utils import *


class LoginAPIView(APIView):
    """
    API that allows users login and get unique Token.
    """
    authentication_classes = (BasicAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = LoginViewSerializer

    def post(self, request, format=None):
        username = request.data["username"]
        password = request.data["password"]

        account = authenticate(username=username, password=password)

        if account is not None:
            if account.is_active:
                token = Token.objects.get_or_create(user=account)[0]
                data = dict()
                data['Authorization'] = "Token %s" % token
                if account.profilemodel.is_verified:
                    profile = ProfileSerializer(account.profilemodel).data

                    for key in profile:
                        data[key] = profile[key]
                    data['course'] = group_year(account.profilemodel.student_group.date_started)
                    response = create_response_scelet("success","User has been logged in", data)
                    return Response(response, status=status.HTTP_200_OK)
                else:
                    response = create_response_scelet('success','User is not verified', data)
                    return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = create_response_scelet('failure', 'Невірний номер телефону чи пароль', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class RegisterAPIView(APIView):
    """
    API that allows users to register a new account.
    """
    permission_classes = (AllowAny,)
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = RegisterViewSerializer

    def post(self, request, format=None):
        # obligatory fields
        username = request.data["username"]
        password = request.data["password"]
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        c_password = request.data['confirm_password']
        birthday = request.data['birthday']
        group_title = request.data['group_title']
        group_started = request.data['group_started']
        faculty = request.data['faculty']
        email = request.data['email']
        photo = request.FILES['photo']

        faculty = FacultyModel.objects.filter(title=faculty)
        user_group = StudentGroupModel.objects.filter(
            title=group_title,
            date_started=group_started
        )
        # validation user input
        if photo.size > (4096*1024):
            response = create_response_scelet('failure', 'Розмір фото перевищує 4МБ', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        try:
            is_valid_image(photo)
        except Exception:
            response = create_response_scelet('failure', 'Формат фото не підтримується', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if User.objects.filter(username=username):
            response = create_response_scelet('failure', 'Такий номер телефону вже зареєстрований', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if User.objects.filter(email=email):
            response = create_response_scelet('failure', 'Така адреса електронної пошти вже зареєстрована', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if password != c_password:
            response = create_response_scelet('failure', 'Паролі не співпадають', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if not faculty:
            response = create_response_scelet('failure', 'Введеного факультету не існує', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)

        if not user_group:
            response = create_response_scelet('failure', 'Введена група не існує', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)


        serialized = UserSerializer(data=request.data).is_valid()

        if serialized:
                new_user = User.objects.create_user(
                    username=username,
                    password=password,
                    first_name=first_name,
                    last_name=last_name,
                    email=email
                )
                new_user.save()

                new_user_profile = ProfileModel(
                    user=new_user,
                    is_student=True,
                    student_group=user_group[0],
                    faculty=faculty[0],
                    started_date=group_started,
                    birthday=birthday,
                    contact_phone=prettify_phone(username),
                    photo=photo
                )
                new_user_profile.save()

                token = Token.objects.get_or_create(user=new_user)[0]
                data = {}
                data['Authorization'] = "Token %s" % token

                response= create_response_scelet('success', 'user has been registered successfully', data)
                return Response(response, status=status.HTTP_201_CREATED)
        else:
            response = create_response_scelet('failure', 'Введені дані не пройшли валідацію', {})
            return Response(response, status=status.HTTP_403_FORBIDDEN)


class AddChatIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AddChatIDSerializer

    def post(self, request):
        user = request.user
        input_chat_id = request.data['chat_id']

        if user.is_active and not user.profilemodel.is_verified:
            if input_chat_id == user.profilemodel.chat_id:
                user.profilemodel.is_verified = True
                user.profilemodel.save()
                user.save()

                token = Token.objects.get_or_create(user=user)[0]
                profile = ProfileSerializer(user.profilemodel).data
                result = dict()
                for key in profile:
                    result[key] = profile[key]
                result['Authorization'] = "Token %s" % token
                result['course'] = group_year(user.profilemodel.student_group.date_started)

                response = create_response_scelet('success', 'Welcome to STUDS community', result)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = create_response_scelet('failure', 'Невіринй код', {})
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class EditProfileView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser, JSONParser)
    serializer_class = EditProfileViewSerializer

    def put(self, request):
        user = request.user
        data = request.data

        if user.is_active:

            if len(request.FILES) != 0:
                user.profilemodel.photo = request.FILES['photo']
            try:
                user.first_name = data['first_name']
            except MultiValueDictKeyError:
                pass

            try:
                user.last_name = data['last_name']
            except MultiValueDictKeyError:
                pass

            try:
                user.profilemodel.middle_name = data['middle_name']
            except MultiValueDictKeyError:
                pass

            try:
                user.email = data['email']
            except MultiValueDictKeyError:
                pass

            try:
                user.profilemodel.birthday = data['birthday']
            except MultiValueDictKeyError:
                pass

            try:
                user.profilemodel.contact_phone = prettify_phone(data['contact_phone'])
            except MultiValueDictKeyError:
                pass

            user.save()
            user.profilemodel.save()
            profile = ProfileSerializer(user.profilemodel).data
            result = dict()
            for key in profile:
                result[key] = profile[key]
            response = create_response_scelet('success', 'Data has been changed', result)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class ChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if user.is_active:
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                response = create_response_scelet('success', 'Пароль успішно змінено', {})
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = create_response_scelet('failure', 'Старий пароль не вірний', {})
                return Response(response, status=status.HTTP_401_UNAUTHORIZED)
        else:
            response = create_response_scelet('failure', 'Не авторизована дія', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)

