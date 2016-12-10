# -*- coding: utf-8 -*-

# import rest framework services
from rest_framework.authentication import (
    TokenAuthentication,
    BasicAuthentication)
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView

# import db models serializers
from mainapp.serializers.serializer import (
    NewsListSerializer,
    NewsContentSerializer,
    CommentViewSerializer
)
# import Serializers For DOCS
from mainapp.serializers.docs_serializer import (
    NewsContentSerializer as d_content,
    LikeNewsSerializer,
    CommentSerializer,
    CreateCommentSerializer,
    LikeCommentsSerializer
)

# import needed app models
from mainapp.models.news import (
    NewsItemModel,
    LikeNewsModel,
    CommentsModel,
    LikeCommentModel
)

# import my own helper methods
from ..utils.custom_utils import *
from ..utils.pagination import PageNumberTPagination


class NewsContentView(APIView):
    authentication_classes = (TokenAuthentication,)
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
    authentication_classes = (TokenAuthentication,)
    pagination_class = PageNumberTPagination
    serializer_class = NewsListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset = NewsItemModel.objects.all().order_by('-created')
        return queryset


class LikeNewsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
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
            if created:
                like.save()
                serializer = NewsListSerializer(item[0])
                response = create_response_scelet('success', 'created', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            if not created:
                like.value = int(value)
                like.save()
                serializer = NewsListSerializer(item[0])
                response = create_response_scelet('success', 'changed', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class CommentsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CommentSerializer

    def post(self, request):
        news_id = request.data['news_id']
        news = NewsItemModel.objects.filter(id=news_id)

        if news:
            news_item = news[0]
            comments = CommentsModel.objects.filter(news=news_item)

            data = []
            if comments:
                for comment in comments:
                    data.append(CommentViewSerializer(comment).data)

            response = create_response_scelet('success', 'list of comments', data)
            return Response(response, status=status.HTTP_200_OK)

        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)


class CreateUpdateDeleteCommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer

    def post(self, request):
        user = request.user
        news_id = request.data['news_id']
        comment = request.data['comment']
        comment_id = request.data['comment_id']
        delete = request.data['delete']

        if user.is_active and user.profilemodel.is_verified:
            news = NewsItemModel.objects.filter(id=news_id)

            if news:
                news_item = news[0]

                if not delete:
                    new_comment, created = CommentsModel.objects.get_or_create(
                        id=comment_id,
                        user=user,
                        news=news_item,
                        comment=comment
                    )

                    if created:
                        new_comment.save()
                        serializer = CommentViewSerializer(new_comment)
                        response = create_response_scelet('success', 'comment created', serializer.data)
                        return Response(response, status=status.HTTP_201_CREATED)
                    else:
                        new_comment.comment = comment
                        new_comment.save()
                        serializer = CommentViewSerializer(new_comment)
                        response = create_response_scelet('success', 'comment updated', serializer.data)
                        return Response(response, status=status.HTTP_200_OK)

                if delete:
                    item = CommentsModel.objects.filter(
                        id=comment_id,
                        user=user,
                        news=news_item
                    )
                    if item:
                        item.delete()
                        comments = CommentsModel.objects.filter(news=news_item)

                        data = []
                        if comments:
                            for comment in comments:
                                data.append(CommentViewSerializer(comment).data)

                        response = create_response_scelet('success', 'comment deleted', data)
                        return Response(response, status=status.HTTP_200_OK)
                    else:
                        response = create_response_scelet('failed', 'Comment ID not found', {})
                        return Response(response, status=status.HTTP_404_NOT_FOUND)
            else:
                response = create_response_scelet('failed', 'ID not found', {})
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = create_response_scelet('failed', 'Not authorized', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class LikeCommentsView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = LikeCommentsSerializer

    def post(self, request):
        user = request.user
        comment_id = request.data['comment_id']
        value = request.data['value']
        item = CommentsModel.objects.filter(id=comment_id)
        if item:
            like, created = LikeCommentModel.objects.get_or_create(
                user=user,
                comment=item[0],
                value=int(value)
            )
            if created:
                like.save()
                serializer = CommentViewSerializer(item[0])
                response = create_response_scelet('success', 'created', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            if not created:
                like.value = int(value)
                like.save()
                serializer = CommentViewSerializer(item[0])
                response = create_response_scelet('success', 'changed', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)