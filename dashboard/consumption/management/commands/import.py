from django.core.management.base import BaseCommand,CommandError
import pandas as pd
import os
from consumption.models import Area,Tariff,UserData,UserConsumption
from django.utils import timezone
from dashboard.settings import PROJECT_PATH

class Command(BaseCommand):
    help = 'import data'
    # def add_argument(self,parser):
    #     parser.add_argument('user_data_csv_path')
    #     parser.add_argument('consumption_csv_path')
    def handle(self, *args, **options):

    #   usr_dt_csv_path = options['user_data_csv_path']
    #   consump_csv_path = options['consumption_csv_path']

        usr_dt_csv_path = os.path.join(PROJECT_PATH, 'data/user_data.csv')
        consump_csv_path =os.path.join(PROJECT_PATH, 'data/consumption/')

        user_df = pd.read_csv(usr_dt_csv_path, encoding='utf8', engine='python')
        unq_area_df = user_df[['area']].drop_duplicates()
        unq_tariff_df = user_df[['tariff']].drop_duplicates()

        db_area_df = pd.DataFrame(list(Area.objects.all().values()))
        db_tariff_df = pd.DataFrame(list(Tariff.objects.all().values()))

        #get data from db. insert data from csv if not in db
        if (db_area_df.empty):
            insrt_area_df = unq_area_df
        else:
            db_area_df = db_area_df[['area']]
            insrt_area_df = pd.concat([unq_area_df,db_area_df])
            insrt_area_df = insrt_area_df.drop_duplicates(keep=False)

        if (db_tariff_df.empty):
            insrt_tariff_df = unq_tariff_df
        else:
            db_tariff_df=db_tariff_df[['tariff']]
            insrt_tariff_df = pd.concat([unq_tariff_df,db_tariff_df])
            insrt_tariff_df = insrt_tariff_df.drop_duplicates(keep=False)

        insrt_area =[Area(area=ar) for ar in insrt_area_df['area'].tolist()]
        insrt_tariff =[Tariff(tariff=tr) for tr in insrt_tariff_df['tariff'].tolist()]

        Area.objects.bulk_create(insrt_area)
        Tariff.objects.bulk_create(insrt_tariff)

        area_df = pd.DataFrame(list(Area.objects.all().values()))
        area_dict = dict(zip(area_df.area,area_df.area_id))
        tariff_df = pd.DataFrame(list(Tariff.objects.all().values()))
        tariff_dict = dict(zip(tariff_df.tariff,tariff_df.tariff_id))

        user_df.replace({'area':area_dict,'tariff':tariff_dict},inplace=True)
        db_user_df = pd.DataFrame(list(UserData.objects.all().values()))
        db_user_df.rename(columns={'area_id':'area','tariff_id':'tariff','user_id':'id'},inplace=True)

        insrt_user_df = pd.concat([user_df,db_user_df])
        insrt_user_df = insrt_user_df.drop_duplicates(keep=False)

        if not(insrt_user_df.empty):
            insrt_user = [UserData(user_id=row['id'],area=Area.objects.get(area_id=row['area']),
                                    tariff=Tariff.objects.get(tariff_id=row['tariff']))
                                    for index,row in insrt_user_df.iterrows()]
            UserData.objects.bulk_create(insrt_user)

        #get all user_consumpt data and insert in bulk
        insrt_usr_cnsmp=[]
        for fl in os.listdir(consump_csv_path):
            usr = UserData.objects.get(user_id=fl.split('.csv')[0])
            usr_cnsmp_path = os.path.join(consump_csv_path,fl)
            usr_cnsmp_df = pd.read_csv(usr_cnsmp_path,encoding='utf8', engine='python')
            usr_cnsmp_df.fillna(0,inplace=True)
            usr_cnsmp = [UserConsumption(user=usr,cnsmpt_date = row['datetime'],
                                        consumption=row['consumption'],created_date=timezone.now())
                                        for index,row in usr_cnsmp_df.iterrows()]
            insrt_usr_cnsmp.extend(usr_cnsmp)

        UserConsumption.objects.bulk_create(insrt_usr_cnsmp)
