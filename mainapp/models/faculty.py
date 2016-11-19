from __future__ import unicode_literals
from django.db import models

from ..utils.custom_utils import group_year


class FacultyModel(models.Model):
    """
    Faculty Model
    """

    class Meta(object):
        verbose_name = u"Факультет"
        verbose_name_plural = u"Факультети"

    title = models.CharField(
        max_length=256,
        blank=True,
        verbose_name=u"Назва",
    )

    dean = models.ForeignKey(
        'mainapp.ProfileModel',
        verbose_name=u"Декан",
        null=True,
        blank=True,
    )

    faculty_address = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name=u"Адреса",
    )

    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title


class DepartmentModel(models.Model):
    """
    Department Model
    """

    class Meta(object):
        verbose_name = u"Кафедра"
        verbose_name_plural = u"Кафедри"

    faculty = models.ForeignKey(
        'FacultyModel',
        verbose_name=u"Факультет",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва",
    )

    leader = models.ForeignKey(
        'mainapp.ProfileModel',
        verbose_name=u"Завідувач",
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title


class Rooms(models.Model):
    """
    model for that saves all rooms
    """

    class Meta(object):

        verbose_name = u"Аудиторія"
        verbose_name_plural = u"Аудиторії"

    faculty = models.ForeignKey(
        FacultyModel,
        blank=False,
        verbose_name=u"Факультет"
    )

    room = models.CharField(
        verbose_name=u"Аудиторія",
        blank=False,
        max_length=10)

    def __unicode__(self):
        return u"%s" % self.room

    def __str__(self):
        return u"%s" % self.room


class StudentGroupModel(models.Model):
    """
    Students Group Model
    """

    class Meta(object):
        verbose_name = u"Група"
        verbose_name_plural = u"Групи"

    department = models.ForeignKey(
        'DepartmentModel',
        verbose_name=u"Кафедра",
    )

    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=u"Назва"
    )

    leader = models.ForeignKey(
        'mainapp.ProfileModel',
        verbose_name=u"Староста",
        related_name='group',
        blank=True,
        null=True,
    )

    date_started = models.DateField(
        verbose_name=u"Дата створення"
    )

    def __unicode__(self):
        return u"%s, %s" % (self.title, group_year(self.date_started))

    def __str__(self):
        return u"%s, %s" % (self.title, group_year(self.date_started))


class Disciplines(models.Model):
    """
    model for that saves all disciplines
    """

    class Meta(object):

        verbose_name = u"Дисципліна"
        verbose_name_plural = u"Дисципліни"

    discipline = models.CharField(
        verbose_name=u"Дисципліна",
        blank=False,
        max_length=255)

    def __unicode__(self):
        return u"%s" % self.discipline

    def __str__(self):
        return u"%s" % self.discipline


class ParaTime(models.Model):

    class Meta(object):
        verbose_name = u"Тривалість пари"
        verbose_name_plural = u"Тривалість пар"

    para_starttime = models.TimeField(
        blank=True,
        null=True,
        verbose_name=u"Початок")

    para_endtime = models.TimeField(
        blank=True,
        null=True,
        verbose_name=u"Завершення"
    )
    para_position = models.IntegerField(
        blank=True,
        null=True,
        default=0,
        verbose_name=u"Номер"
    )

    faculty = models.ForeignKey(
        FacultyModel,
        verbose_name="Факультет"
    )

    def __unicode__(self):
        return u"%s: %s-%s" % (self.para_position, self.para_starttime, self.para_endtime)

    def __str__(self):
        return u"%s: %s-%s" % (self.para_position, self.para_starttime, self.para_endtime)


class Para(models.Model):

    class Meta(object):
        verbose_name = u"Пара"
        verbose_name_plural = u"Розклад"

    para_subject = models.ForeignKey(
        'Disciplines',
        blank=True,
        null=True,
        verbose_name=u"Дисципліна"
    )
    para_room = models.ForeignKey(
        'Rooms',
        blank=True,
        null=True,
        verbose_name=u"Аудиторія"
    )
    para_professor = models.ForeignKey(
        'mainapp.ProfileModel',
        blank=True,
        null=True,
        verbose_name=u"Викладач"
    )
    para_number = models.ForeignKey(
        'ParaTime',
        blank=True,
        null=True,
        verbose_name=u"Номер пари"
    )
    para_day = models.ForeignKey(
        'mainapp.WorkingDay',
        blank=True,
        null=True,
        verbose_name=u"День")

    para_group = models.ForeignKey(
        'StudentGroupModel',
        blank=True,
        null=True,
        verbose_name=u"Група"
    )
    week_type = models.BooleanField(
        default=True,
        verbose_name=u"Парний тиждень"
    )
    semester = models.ForeignKey(
        'StartSemester',
        blank=True,
        verbose_name=u"Семестр"
    )

    def __unicode__(self):
        return u"%s %s" % (self.para_subject, self.para_room)

    def __str__(self):
        return u"%s %s" % (self.para_subject, self.para_room)

