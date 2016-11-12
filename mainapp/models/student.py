from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User


class StudentJournalModel(models.Model):
    """
    Saves student marks that they get during classes/modules
    """

    class Meta(object):
        verbose_name = u"Student Journal"
        verbose_name_plural = u"Student Journal"

    value = models.CharField(
        max_length=55,
        blank=True,
        null=True,
        verbose_name="Value",
        default=''
    )
    date = models.DateField(
        verbose_name="Date"
    )
    discipline = models.ForeignKey(
        'mainapp.Disciplines',
        verbose_name="Discipline"
    )
    para_number = models.ForeignKey(
        'mainapp.ParaTime',
        verbose_name="Class #"
    )
    student = models.ForeignKey(
        User,
        verbose_name="Student"
    )
    is_module = models.BooleanField(
        verbose_name="Module value"
    )

    def __str__(self):
        return u"%s" % self.student.get_full_name()

    def __unicode__(self):
        return u"%s" % self.student.get_full_name()
