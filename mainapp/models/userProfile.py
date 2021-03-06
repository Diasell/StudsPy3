# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)


class ProfileModel(models.Model):
    """
    Students Profile model
    """

    user = models.OneToOneField(User, primary_key=True)

    is_student = models.BooleanField(
        verbose_name=u"Студент",
        default=True,
    )

    is_professor = models.BooleanField(
        verbose_name=u"Викладач",
        default=False,
        blank=True
    )

    is_staff = models.BooleanField(
        verbose_name="Персонал",
        default=False,
        blank=True
    )

    started_date = models.DateField(
        auto_now_add=True,
        verbose_name=u"Дата початку навчання"
    )

    faculty = models.ForeignKey(
        'mainapp.FacultyModel',
        verbose_name=u"Факультет",
        blank=True,
        null=True,
    )

    department = models.ForeignKey(
        'mainapp.DepartmentModel',
        verbose_name=u"Кафедра",
        blank=True,
        null=True,
    )

    student_group = models.ForeignKey(
        'mainapp.StudentGroupModel',
        verbose_name=u"Група",
        blank=True,
        null=True,
    )

    middle_name = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"По-батькові",
        default='')

    birthday = models.DateField(
        blank=True,
        verbose_name=u"Дата народження",
        null=True)

    contact_phone = models.CharField(
        max_length=55,
        blank=True,
        verbose_name=u"тел",
        null=True,
    )

    photo = models.ImageField(
        blank=True,
        verbose_name=u"Фото",
        upload_to=user_directory_path,
        null=True)

    chat_id = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Telegram Chat ID",
        null=True
    )

    is_verified = models.BooleanField(
        default=False,
        verbose_name=u"Аккакунт підтверджений"
    )

    room = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        verbose_name=u"Аудиторія"
    )

    def __unicode__(self):
        if self.is_student:
            return u"Student: %s" % self.user.get_full_name()
        elif self.is_professor:
            return u"Professor: %s" % self.user.get_full_name()
        else:
            return u"Staff Member: %s" % self.user.get_full_name()

    def __str__(self):
        if self.is_student:
            return u"Student: %s" % self.user.get_full_name()
        elif self.is_professor:
            return u"Professor: %s" % self.user.get_full_name()
        else:
            return u"Staff Member: %s" % self.user.get_full_name()
