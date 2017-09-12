# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client
from consumption.models import Area,Tariff,UserData,UserConsumption
import allexceptions as ex
import datetime as dt

# Create your tests here.

class CheckRoutes(TestCase):
    def setup(self):
        self.client = Client()

    def create_objs(self):
        Area.objects.create(area_id=5, area='a5')
        Area.objects.create(area_id=6, area='a6')
        Tariff.objects.create(tariff_id=8, tariff='t8')
        Tariff.objects.create(tariff_id=9, tariff='t9')
        UserData.objects.create(user_id=1000, area=Area.objects.get(area='a5'), tariff=Tariff.objects.get(tariff='t8'))
        UserData.objects.create(user_id=1001, area=Area.objects.get(area='a6'), tariff=Tariff.objects.get(tariff='t9'))
        UserConsumption.objects.create(user=UserData.objects.get(user_id=1000), cnsmpt_date=dt.date(2016, 8, 12), consumption=35,created_date=dt.datetime.now())
        UserConsumption.objects.create(user=UserData.objects.get(user_id=1000), cnsmpt_date=dt.date(2016, 8, 13), consumption=35,created_date=dt.datetime.now())
        UserConsumption.objects.create(user=UserData.objects.get(user_id=1001), cnsmpt_date=dt.date(2016, 8, 12), consumption=35,created_date=dt.datetime.now())
        UserConsumption.objects.create(user=UserData.objects.get(user_id=1001), cnsmpt_date=dt.date(2016, 8, 14), consumption=35,created_date=dt.datetime.now())

    def test_routes(self):
        self.create_objs()
        with self.assertRaises(ex.DateNotProvidedError) as err:
            resp_summary = self.client.get('/')

        excp_msg = err.exception
        self.assertEqual(excp_msg.message,"Date not provided")

        resp_summary = self.client.get('/summary/',{'start_date':'2016-08-12','end_date':'2016-08-20'})
        self.assertEqual(resp_summary.status_code,200)

        with self.assertRaises(ex.NoDataFound) as err:
            resp_summary = self.client.get('/summary/',{'start_date':'2016-08-09','end_date':'2016-08-11'})
        self.assertEqual(err.exception.message, "No data found")

        resp_summary = self.client.get('/detail/', {'start_date': '2016-08-12', 'end_date': '2016-08-20','user_id':'1000'})
        self.assertEqual(resp_summary.status_code, 200)


