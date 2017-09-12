# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse
from consumption.models import UserData
import pandas as pd
import  json
import allexceptions as ex
from . import process

# Create your views here.

def summary(request):
  start_date = request.GET.get('start_date', '')
  end_date = request.GET.get('end_date', '')

  if ((start_date is None) or (not start_date) or (end_date is None) or (not end_date)) :
    raise ex.DateNotProvidedError("Date not provided")

  tot_cnsmpt=process.get_tot_consumpt(start_date=start_date,end_date=end_date)
  usr_tot_consumpt = process.get_tot_user_consumpt(start_date=start_date,end_date=end_date)

  context = {
      'message': 'Hello!',
      'summ_data': tot_cnsmpt,
      'users_data' : usr_tot_consumpt
  }
  return render(request, 'consumption/summary.html', context)

def detail(request):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')
    user_id = request.GET.get('user_id', '')

    if ((start_date is None) or (not start_date) or (end_date is None) or (not end_date)):
        raise ex.DateNotProvidedError("Date not provided")

    if ((user_id is None)or(not user_id)):
        raise ex.UserNotProvided("USer not provided")

    usr_consumpt = process.get_user_consumpt(user_id=user_id, start_date=start_date, end_date=end_date)

    usr_dets = {'user_id':usr_consumpt[0]['user_id'],'area':usr_consumpt[0]['user__area__area'],'tariff':usr_consumpt[0]['user__tariff__tariff']}

    usr_consumpt_json = json.dumps(usr_consumpt)
    context = {
    'u_data':usr_consumpt_json,
    'usr_dt':    usr_dets
        }
    return render(request, 'consumption/detail.html', context)

def date_summary(request):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    if ((start_date is None) or (not start_date) or (end_date is None) or (not end_date)):
        raise ex.DateNotProvidedError("Date not provided")

    out_data = process.get_tot_user_consumpt(start_date=start_date,end_date=end_date)

    for o_data in out_data:
        area_trf = process.get_area_tariff(o_data['user_id'])
        o_data.update({'area': area_trf['area__area']})
        o_data.update({'tariff':area_trf['tariff__tariff']})

    out_data_df = pd.DataFrame(out_data)
    area_df = out_data_df[['area','val']]
    tariff_df = out_data_df[['tariff','val']]
    area_data_grouped = area_df.groupby(['area']).agg(sum)
    tariff_data_grouped= tariff_df.groupby(['tariff']).agg(sum)

    area_dict = area_data_grouped.reset_index().to_dict('records')
    tariff_dict = tariff_data_grouped.reset_index().to_dict('records')

    top_data = sorted(out_data,key = lambda i:i['val'],reverse=True)[:5]

    return HttpResponse(json.dumps({"top_data":top_data,"area_data":area_dict,"tariff_data":tariff_dict}))