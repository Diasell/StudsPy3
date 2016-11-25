# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class StartSemester(models.Model):

    class Meta(object):
        verbose_name = u"Розклад Семестрів"
        verbose_name_plural = u"Розклад Семестрів"

    title = models.CharField(max_length=255,
                             blank=False,
                             null=True,
                             default=u"1й семестр",
                             verbose_name=u"Семестр")
    semesterstart = models.DateField(verbose_name=u"Починається")
    semesterend = models.DateField(verbose_name=u"Завершується")

    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title


class WorkingDay(models.Model):

    class Meta(object):
        verbose_name = u"День"
        verbose_name_plural = u"Робочі дні"

    dayoftheweek = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        verbose_name=u"День тижня")
    dayoftheweeknumber = models.IntegerField(
        blank=True,
        null=True,
        verbose_name=u"Номер"
    )

    def __unicode__(self):
        return u"%s" % self.dayoftheweek

    def __str__(self):
        return u"%s" % self.dayoftheweek
