# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models


def upload_location(instance, filename):
    return "news/%s/%s" % (instance.title, filename)


class NewsItemModel(models.Model):

    class Meta(object):
        verbose_name = u"Новина"
        verbose_name_plural = u"НОВИНИ"

    author = models.ForeignKey(
        User,
        verbose_name=u'Автор'
    )

    title = models.CharField(
        max_length=500,
        blank=False,
        verbose_name=u"Заголовок"
    )
    title_image = models.ImageField(
        upload_to=upload_location,
        blank=True,
        verbose_name=u"Картинка"
    )
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name=u"Змінено")
    created = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name=u"Створено")

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title
