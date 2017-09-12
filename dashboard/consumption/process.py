from consumption.models import UserConsumption,UserData
from django.db.models import Sum
from django.db.models.functions import TruncDay
import  json
import pandas as pd
import allexceptions as ex

#sum of cunsumption for all users for given date range. output as date and tot_consumption(groupby date)
def get_tot_consumpt(start_date,end_date):
    tot_cnsmpt= UserConsumption.objects.filter(cnsmpt_date__gte=start_date,cnsmpt_date__lt=end_date)\
        .extra({'cnsmpt_date':"date(cnsmpt_date)"}).values('cnsmpt_date').annotate(val=Sum('consumption'))
    if not tot_cnsmpt.exists():
        raise  ex.NoDataFound("No data found")
    tot_cnsmpt=json.dumps(list(tot_cnsmpt))
    return tot_cnsmpt

#sum of cunsumption for all users for given date range. output as user and tot_consumption(groupby user)
def get_tot_user_consumpt(start_date,end_date):
    usr_tot_consumpt = UserConsumption.objects.filter(cnsmpt_date__gte=start_date,cnsmpt_date__lt=end_date)\
        .values('user_id').annotate(val=Sum('consumption'))
    if not usr_tot_consumpt.exists():
        raise  ex.NoDataFound("No data found")
    usr_tot_consumpt = list(usr_tot_consumpt)
    return usr_tot_consumpt

#daywise consumption for a user for given date range. output as user,date,area,tariff,consumption
def get_user_consumpt(user_id,start_date,end_date):
    usr_consumpt = UserConsumption.objects.filter(cnsmpt_date__gte=start_date,cnsmpt_date__lt=end_date,user=user_id).extra({'cnsmpt_date':"date(cnsmpt_date)"})\
        .values('user_id','cnsmpt_date','user__area__area','user__tariff__tariff').annotate(val=Sum('consumption'))
    if not usr_consumpt.exists():
        raise  ex.NoDataFound("No data found")
    usr_consumpt=list(usr_consumpt)
    return usr_consumpt

#get area and tariff for given user
def get_area_tariff(user_id):
    out_data=list(UserData.objects.filter(user_id=user_id).values('area__area', 'tariff__tariff'))[0]
    return out_data

#sum of consumption for given date range. output as date,area/tariff,consumption
def get_all_consumpt(start_date,end_date):
    all_consumpt = list(UserConsumption.objects.filter(cnsmpt_date__gte=start_date,cnsmpt_date__lt=end_date)
                        .values('cnsmpt_date','consumption','user__area__area','user__tariff__tariff'))
    all_consumpt = pd.DataFrame(all_consumpt)
    area_df = all_consumpt[['cnsmpt_date','consumption','user__area__area']]
    tariff_df = all_consumpt[['cnsmpt_date','consumption','user__tariff__tariff']]
    all_consumpt_area = area_df.groupby(['cnsmpt_date','user__area__area']).agg(sum)
    # all_consumpt_tariff = tariff_df.groupby(['cnsmpt_date', 'user__tariff__tariff']).agg(sum)
    # print all_consumpt_area
