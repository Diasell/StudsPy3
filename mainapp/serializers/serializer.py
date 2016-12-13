from django.contrib.auth.models import User
from rest_framework import serializers

from mainapp.models.userProfile import ProfileModel
from mainapp.models.helpermodels import WorkingDay
from mainapp.models.student import StudentJournalModel
from mainapp.models.news import (
    NewsItemModel,
    LikeNewsModel,
    CommentsModel,
    LikeCommentModel
)
from mainapp.models.faculty import (
    FacultyModel,
    DepartmentModel,
    StudentGroupModel,
    Para,
    ParaTime,
    Disciplines
)


class StudentJournalSerializer(serializers.ModelSerializer):
    student = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='username'
    )
    discipline = serializers.SlugRelatedField(
        queryset=Disciplines.objects.all(),
        slug_field='discipline'
    )
    para_number = serializers.SlugRelatedField(
        queryset=ParaTime.objects.all(),
        slug_field='para_position'
    )

    class Meta:
        model = StudentJournalModel
        fields = (
            'pk',
            'value',
            'date',
            'discipline',
            'para_number',
            'student',
            'is_module'
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name'
        )


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer class for the Profile Model
    """

    username = serializers.CharField(
        source='user.username',
        read_only=True,
    )
    email = serializers.EmailField(
        source='user.email',
        read_only=True,
    )
    last_name = serializers.CharField(
        source='user.last_name',
        read_only=True
    )
    first_name = serializers.CharField(
        source='user.first_name',
        read_only=True
    )
    faculty = serializers.CharField(
        source='faculty.title',
        read_only=True,
    )
    department = serializers.CharField(
        source='department.title',
        read_only=True
    )
    student_group = serializers.CharField(
        source='student_group.title'
    )

    class Meta:
        model = ProfileModel
        fields = (
            'username',
            'email',
            'last_name',
            'first_name',
            'middle_name',
            'is_student',
            'is_professor',
            'faculty',
            'department',
            'student_group',
            'contact_phone',
            'birthday',
            'photo',
            'started_date',
            'is_verified'
        )


class StudentGroupSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source='department.title',
        read_only=True,
    )
    leader = serializers.CharField(
        source='leader.user.last_name',
        read_only=True
    )
    mentor = ProfileSerializer()

    class Meta:
        model = StudentGroupModel

        fields = (
            'title',
            'department',
            'leader',
            'mentor',
            'date_started'
        )


class FacultySerializer(serializers.ModelSerializer):
    dean = UserSerializer(read_only=True)

    class Meta:
        model = FacultyModel
        fields = (
            'title',
            'dean',
            'department_address'
        )


class DepartmentSerializer(serializers.ModelSerializer):
    faculty = FacultySerializer()
    leader = UserSerializer(read_only=True)

    class Meta:
        model = DepartmentModel
        fields = (
            'faculty',
            'title',
            'leader'
        )


class ParaTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParaTime
        fields = (
            'para_starttime',
            'para_endtime',
            'para_position'
        )


class WorkingDaySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingDay
        fields = (
            'dayoftheweek',
        )


class ParaSerializer(serializers.ModelSerializer):
    """
    Serializer for the Para Model
    """
    discipline = serializers.CharField(
        source='para_subject.discipline',
        read_only=True)
    room = serializers.CharField(
        source='para_room.room',
        read_only=True)
    professors_lastname = serializers.CharField(
        source='para_professor.user.last_name',
        read_only=True)
    professors_firstname = serializers.CharField(
        source='para_professor.user.first_name',
        read_only=True)
    professors_middlename = serializers.CharField(
        source='para_professor.middle_name',
        read_only=True)
    para_number = serializers.CharField(
        source='para_number.para_position',
        read_only=True)
    para_day = serializers.CharField(
        source='para_day.dayoftheweek',
        read_only=True)
    para_group = serializers.CharField(
        source='para_group.title')
    start_time = serializers.DateTimeField(
        source='para_number.para_starttime',
        read_only=True)
    end_time = serializers.DateTimeField(
        source='para_number.para_endtime',
        read_only=True)

    class Meta:
        model = Para
        fields = (
            'discipline',
            'room',
            'professors_lastname',
            'professors_firstname',
            'professors_middlename',
            'para_number',
            'start_time',
            'end_time',
            'para_day',
            'para_group',
            'week_type'
        )


class NewsListSerializer(serializers.ModelSerializer):
    class Meta(object):
        model = NewsItemModel
        fields = (
            'id',
            'title',
            'title_image',
            'created'
        )



class NewsContentSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField('get_news_likes')

    class Meta(object):
        model = NewsItemModel
        fields = (
            'id',
            'title',
            'title_image',
            'content',
            'updated',
            'created',
            'likes'
        )

    def get_news_likes(self, object):
        result = 0
        queryset = LikeNewsModel.objects.filter(news=object)
        if queryset:
            for item in queryset:
                result += int(item.value)
        return result


class NewsListSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField('get_news_likes')
    user_like = serializers.SerializerMethodField()

    class Meta(object):
        model = NewsItemModel
        fields = (
            'id',
            'title',
            'title_image',
            'created',
            'likes',
            'user_like'
        )

    def get_news_likes(self, object):
        total = 0
        likes = 0
        dislikes = 0
        queryset = LikeNewsModel.objects.filter(news=object)
        if queryset:
            for item in queryset:
                total += int(item.value)
                if item.value == 1:
                    likes += int(item.value)
                elif item.value == -1:
                    dislikes += int(item.value)
        result = {'total': total, 'likes': likes, 'dislikes': dislikes}
        return result

    def get_user_like(self, object):
        try:
            user = self.context['request'].user
            like = LikeNewsModel.objects.filter(news=object, user=user)
            if like:
                return like[0].value
        except KeyError:
            return None


class CommentViewSerializer(serializers.ModelSerializer):

    likes = serializers.SerializerMethodField('get_comment_likes')
    full_name = serializers.CharField(source='user.get_full_name')

    class Meta(object):
        model = CommentsModel
        fields = (
            'id',
            'full_name',
            'news',
            'comment',
            'created',
            'likes'
        )


    def get_comment_likes(self, object):
        result = 0
        queryset = LikeCommentModel.objects.filter(comment=object)
        if queryset:
            for item in queryset:
                result += int(item.value)
        return result
