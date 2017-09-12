# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Area(models.Model):
    area_id = models.AutoField(primary_key=True)
    area = models.CharField(max_length=5)

    class Meta:
        db_table = 'area'

    def __str__(self):
        return str(self.area_id)

class Tariff(models.Model):
    tariff_id = models.AutoField(primary_key=True)
    tariff = models.CharField(max_length=5)

    class Meta:
        db_table='tariff'

    def __str__(self):
        return str(self.tariff_id)

class UserData(models.Model):
    user_id = models.IntegerField(unique=True)
    area = models.ForeignKey('consumption.Area')
    tariff = models.ForeignKey('consumption.Tariff')

    class Meta:
        db_table='user_data'

    def __str__(self):
        return str(self.user_id)

class UserConsumption(models.Model):
    user = models.ForeignKey('consumption.UserData',to_field='user_id')
    cnsmpt_date = models.DateTimeField()
    consumption = models.FloatField()
    created_date = models.DateTimeField()

    class Meta:
        db_table='user_consumption'

    def __str__(self):
        return u'%s %s %s' %(self.user_id,self.cnsmpt_date,self.consumption)
