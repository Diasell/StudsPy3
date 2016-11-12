from __future__ import unicode_literals
from django.db import models

class StartSemester(models.Model):

    class Meta(object):
        verbose_name = u"Semester schedule"
        verbose_name_plural = u"Semester's schedule"

    title = models.CharField(max_length=255,
                             blank=False,
                             null=True,
                             default=u"1st Semester",
                             verbose_name=u"Semester")
    semesterstart = models.DateField(verbose_name=u"Start at")
    semesterend = models.DateField(verbose_name=u"Ends")

    def __unicode__(self):
        return u"%s" % self.title

    def __str__(self):
        return u"%s" % self.title


class WorkingDay(models.Model):

    class Meta(object):
        verbose_name = u"Day"
        verbose_name_plural = u"Days"

    dayoftheweek = models.CharField(max_length=50, blank=True, null=True)
    dayoftheweeknumber = models.IntegerField(
        blank=True,
        null=True
    )

    def __unicode__(self):
        return u"%s" % self.dayoftheweek

    def __str__(self):
        return u"%s" % self.dayoftheweek
