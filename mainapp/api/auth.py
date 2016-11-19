#  import django services
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

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
    LoginViewSerializer)

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
                return Response(result, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Username/password combination is invalid'
                },
                status=status.HTTP_401_UNAUTHORIZED
            )


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
                {'Failed': 'image size is greater than 4MB'},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            is_valid_image(photo)
        except Exception:
            return Response(
                {'Failed': "attachment format is not supported"},
                status=status.HTTP_403_FORBIDDEN
            )

        if User.objects.filter(username=username):
            return Response(
                {'Failed': "username is already taken"},
                status=status.HTTP_403_FORBIDDEN
            )
        if User.objects.filter(email=email):
            return Response(
                {'Failed': "email is already taken"},
                status=status.HTTP_403_FORBIDDEN
            )
        if password != c_password:
            return Response({
                'Failed': "passwords doesn't match"},
                status=status.HTTP_403_FORBIDDEN
            )
        if not faculty:
            return Response({
                'Failed': "user faculty is not valid"},
                status=status.HTTP_403_FORBIDDEN
            )
        if not user_group:
            return Response({
                'Failed': "user group is not valid"},
                status=status.HTTP_403_FORBIDDEN
            )

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
                    photo=photo
                )
                new_user_profile.save()

                token = Token.objects.get_or_create(user=new_user)[0]
                profile = ProfileSerializer(new_user_profile).data
                response = dict()
                for key in profile:
                    response[key] = profile[key]
                response['Authorization'] = "Token %s" % token
                response['full_name'] = new_user.get_full_name()

                return Response(response, status=status.HTTP_201_CREATED)
        else:
            return Response({
                'status': 'Unauthorized',
                'message': 'Provided data is invalid'
                },
                status=status.HTTP_403_FORBIDDEN
            )

