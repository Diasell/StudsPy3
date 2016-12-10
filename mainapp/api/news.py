# -*- coding: utf-8 -*-
#  import django services
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
from rest_framework.generics import ListAPIView

# import db models serializers
from mainapp.serializers.serializer import (
    NewsListSerializer,
    NewsContentSerializer)
from mainapp.serializers.docs_serializer import (
    NewsContentSerializer as d_content,

)

# import needed app models
from mainapp.models.news import (
    NewsItemModel,
    LikeNewsModel)

# import my own helper methods
from ..utils.custom_utils import *
from ..utils.pagination import PageNumberTPagination


class NewsContentView(APIView):
    authentication_classes = (IsAuthenticated,)
    permission_classes = (IsAuthenticated,)
    serializer_class = d_content

    def post(self, request, format=None):
        news_id = request.data['id']

        item = NewsItemModel.objects.filter(id=news_id)

        if item:
            data = NewsContentSerializer(item[0]).data
            response = create_response_scelet('success', 'Content message', data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)



class NewsListView(ListAPIView):
    authentication_classes = (IsAuthenticated,)
    pagination_class = PageNumberTPagination
    serializer_class = NewsListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = NewsItemModel.objects.all().order_by('-created')
        return queryset


class LikeNewsView(APIView):
    authentication_classes = (IsAuthenticated,)
    serializer_class = LikeNewsSerializer

    def post(self, request):
        user = request.user
        news_id = request.data['id']
        value = request.data['value']
        item = NewsItemModel.objects.filter(id=news_id)
        if item:
            like, created = LikeNewsModel.objects.get_or_create(
                user=user,
                news=item[0],
                value=int(value)
            )
            serializer = NewsListSerializer(item[0])

            if created:
                like.save()
                response = create_response_scelet('success', 'got it', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            if not created:
                like.value = int(value)
                like.save()
                response = create_response_scelet('success', 'changed', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)


