from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class StudentJournalModel(models.Model):
    """
    Saves student marks that they get during classes/modules
    """

    class Meta(object):
        verbose_name = u"Результат"
        verbose_name_plural = u"Результати студентів"

    value = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Бал",
        default=''
    )
    date = models.DateField(
        verbose_name="Дата"
    )
    discipline = models.ForeignKey(
        'mainapp.Disciplines',
        verbose_name="Дисципліна"
    )
    para_number = models.ForeignKey(
        'mainapp.ParaTime',
        verbose_name="Номер пари"
    )
    student = models.ForeignKey(
        User,
        verbose_name="Студент"
    )
    is_module = models.BooleanField(
        verbose_name="Модуль"
    )

    def __str__(self):
        return u"%s" % self.student.get_full_name()

    def __unicode__(self):
        return u"%s" % self.student.get_full_name()
