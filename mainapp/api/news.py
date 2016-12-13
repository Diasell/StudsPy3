# -*- coding: utf-8 -*-

# import rest framework services
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
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
    NewsContentSerializerD,
    LikeNewsSerializer,
    CommentSerializer,
    CreateCommentSerializer,
    UpdateCommentSerializer,
    LikeCommentsSerializer,
    DeleteCommentSerializer
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
    serializer_class = NewsContentSerializerD

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

    def get_serializer_context(self):
        return {'request': self.request}


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
            like = LikeNewsModel.objects.filter(
                user=user,
                news=item[0]
            )

            if like:
                like[0].value = int(value)
                like[0].save()
                serializer = NewsListSerializer(item[0])
                response = create_response_scelet('success', 'changed', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            if not like:
                new_like = LikeNewsModel.objects.create(
                    user=user,
                    news=item[0],
                    value=int(value)
                )
                new_like.save()
                serializer = NewsListSerializer(item[0])
                response = create_response_scelet('success', 'created', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
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


class CreateCommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = CreateCommentSerializer

    def post(self, request):
        user = request.user
        news_id = request.data['news_id']
        comment = request.data['text']

        if user.is_active and user.profilemodel.is_verified:
            news = NewsItemModel.objects.filter(id=news_id)

            if news:
                news_item = news[0]
                new_comment = CommentsModel.objects.create(
                    user=user,
                    news=news_item,
                    comment=comment
                )

                new_comment.save()
                serializer = CommentViewSerializer(new_comment)
                response = create_response_scelet('success', 'comment created', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            else:
                response = create_response_scelet('failed', 'ID not found', {})
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = create_response_scelet('failed', 'Not authorized', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class UpdateCommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateCommentSerializer

    def post(self, request):
        user = request.user
        comment_id = request.data['comment_id']
        edited_text = request.data['edited_text']

        if user.is_active and user.profilemodel.is_verified:
            comments = CommentsModel.objects.filter(id=comment_id)

            if comments:
                comment = comments[0]
                comment.comment = edited_text
                comment.save()

                serializer = CommentViewSerializer(comment)
                response = create_response_scelet('success', 'comment has been edited', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
            else:
                response = create_response_scelet('failed', 'comment not found', {})
                return Response(response, status=status.HTTP_404_NOT_FOUND)
        else:
            response = create_response_scelet('failed', 'Not authorized', {})
            return Response(response, status=status.HTTP_401_UNAUTHORIZED)


class DeleteCommentView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = DeleteCommentSerializer

    def delete(self, request):
        user = request.user
        comment_id = request.data['comment_id']

        item = CommentsModel.objects.filter(id=comment_id, user=user)
        if item:
            news = item[0].news
            item[0].delete()
            comments = CommentsModel.objects.filter(news=news)

            data = []
            if comments:
                for comment in comments:
                    data.append(CommentViewSerializer(comment).data)

            response = create_response_scelet('success', 'comment deleted', data)
            return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'Comment ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)


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
            like = LikeCommentModel.objects.filter(
                user=user,
                comment=item[0],
            )

            if not like:
                new_like = LikeCommentModel.objects.create(
                    user=user,
                    comment=item[0],
                    value=int(value)
                )
                new_like.save()
                serializer = CommentViewSerializer(item[0])
                response = create_response_scelet('success', 'created', serializer.data)
                return Response(response, status=status.HTTP_201_CREATED)
            if like:
                like[0].value = int(value)
                like[0].save()
                serializer = CommentViewSerializer(item[0])
                response = create_response_scelet('success', 'changed', serializer.data)
                return Response(response, status=status.HTTP_200_OK)
        else:
            response = create_response_scelet('failed', 'ID not found', {})
            return Response(response, status=status.HTTP_404_NOT_FOUND)
