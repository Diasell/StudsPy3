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
                user = User.objects.get(username=username)
                profile = ProfileSerializer(user.profilemodel).data
                result = dict()
                for key in profile:
                    result[key] = profile[key]
                result['Authorization'] = "Token %s" % token
                result['course'] = group_year(user.profilemodel.student_group.date_started)
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'failure',
                             'message': 'Невірний номер телефону чи пароль'},
                            status=status.HTTP_401_UNAUTHORIZED)


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
            return Response(
                {'status': 'failure',
                 'message': 'Розмір фото перевищує 4МБ'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            is_valid_image(photo)
        except Exception:
            return Response(
                {'status': 'failure',
                 'message': "Формат фото не підтримується"},
                status=status.HTTP_403_FORBIDDEN)

        if User.objects.filter(username=username):
            return Response(
                {'status': 'failure',
                 'message': "Такий номер телефону вже зареєстрований"},
                status=status.HTTP_403_FORBIDDEN)
        if User.objects.filter(email=email):
            return Response(
                {'status': 'failure',
                 'message': "Така адреса електронної пошти вже зареєстрована"},
                status=status.HTTP_403_FORBIDDEN)
        if password != c_password:
            return Response({'status': 'failure',
                             'message': "Паролі не співпадають"},
                            status=status.HTTP_403_FORBIDDEN)
        if not faculty:
            return Response({'status': 'failure',
                             'message': "Введеного факультету не існує"},
                            status=status.HTTP_403_FORBIDDEN)
        if not user_group:
            return Response({
                'status': 'failure',
                'message': "Введена група не існує"},
                status=status.HTTP_403_FORBIDDEN)

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
                    contact_phone=username,
                    photo=photo
                )
                new_user_profile.save()
                token = Token.objects.get_or_create(user=new_user)[0]

                response={}
                data = {}
                response['status'] = 'success'
                data['message'] = 'user has been registered successfully'
                data['Authorization'] = "Token %s" % token
                response['data'] = data

                return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'failure',
                'message': 'Введені дані не пройшли валідацію'
                },
                status=status.HTTP_403_FORBIDDEN)


class AddChatIdView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = AddChatIDSerializer

    def post(self, request):
        user = request.user
        input_chat_id = request.data['chat_id']

        if user.is_active and not user.is_verified:
            if input_chat_id == user.profilemodel.chat_id:
                user.profilemodel.is_verified = True
                user.profilemodel.save()
                user.save()

                token = Token.objects.get_or_create(user=user)[0]
                profile = ProfileSerializer(user.profilemodel).data
                response = dict()
                for key in profile:
                    response[key] = profile[key]
                response['Authorization'] = "Token %s" % token
                response['course'] = group_year(user.profilemodel.student_group.date_started)
                return Response(response, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failure',
                                 'message': 'Невіринй код'},
                                status=status.HTTP_403_FORBIDDEN)

        else:
            return Response({'status': 'failure',
                             'message': 'Не авторизована дія'},
                            status=status.HTTP_401_UNAUTHORIZED)


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
                user.profilemodel.contact_phone = data['contact_phone']
            except MultiValueDictKeyError:
                pass

            user.save()
            user.profilemodel.save()
            profile = ProfileSerializer(user.profilemodel).data
            result = dict()
            for key in profile:
                result[key] = profile[key]
            return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({'status': 'Unauthorized',
                             'message': 'Не авторизовано'},
                            status=status.HTTP_403_FORBIDDEN)


class ChangePasswordView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = ChangePasswordSerializer

    def post(self, request):
        user = request.user
        old_password = user.data['old_password']
        new_password = user.data['new_password']

        if user.is_active:
            if user.check_password(old_password):
                user.set_password(new_password)
                user.save()
                return Response({'status': 'Success',
                                 'message': u'Пароль успішно змінено'},
                                status=status.HTTP_200_OK)
            else:
                return Response({'status': 'failure',
                                 'message': u'Старий пароль не вірний'},
                                status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'status': 'Unauthorized',
                             'message': 'Не авторизовано'},
                            status=status.HTTP_403_FORBIDDEN)


# class ForgotPasswordView(APIView):
#     authentication_classes = (AllowAny,)
#     permission_classes = (AllowAny,)
#     serializer_class = ForgotPasswordViewSerializer
#
#     def post(self, request):
#         username = request.data['username']
#
#         user_filter = User.objects.filter(username=username)
#
#         if len(user_filter)>0:
#             user = user_filter[0]
#             if user.profilemodel.is_verified:
#                 if user.is_active:
#                     temp_password = generate_new_password()
#                     user.set_password(temp_password)
#                     user.save()
#
#                     message=u'Ваш новий пароль:\n' + temp_password
#                     message1 = u"Ви можете змінити його в нашлаштуваннях вашого профілю"
#                     STUDS_TELEGRAM_BOT.send_message(message + message1, user.profilemodel.chat_id)
#
#                     return Response({'status': 'Success',
#                                      'message': 'Новий пароль був надісланий чат ботом'},
#                                     status=status.HTTP_200_OK)
#
#                 else:
#                     return Response({'status': 'Unauthorized',
#                                      'message': 'Аккаунт не активний'},
#                                     status=status.HTTP_403_FORBIDDEN)
#             else:
#                 return Response({'status': 'Unauthorized',
#                                  'message': 'Аккаунт не пройшов верифікацію Telergam ботом'},
#                                 status=status.HTTP_403_FORBIDDEN)
#         else:
#             return Response({'status': 'Unauthorized',
#                              'message': 'Користувача з таким номером телефону не існує'},
#                             status=status.HTTP_403_FORBIDDEN)




