# -*- coding: utf-8 -*-

from django.db import models

class  zhihu(models.Model):
    url = models.CharField('url', max_length=200)
    title = models.CharField('title', max_length=200)

