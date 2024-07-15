from django.shortcuts import render
from projects.models import Project

from rest_framework.parsers import JSONParser
from rest_framework.views import APIView

from projects.models import FishingPlaceInfoData
from projects.fishingram import FishingPlcInfoSerializer

from datetime import datetime
import random
import requests, json

# Create your views here.
def project_index(request):
    return render(request, 'project_index.html')


def project_detail(request, project):
    if project == 'cognitive-services':
        return render(request, 'cognitive-services.html')
    elif project == 'image-processing':
        return render(request, 'image-processing.html')
    elif project == 'object-detection':
        return render(request, 'object-detection.html')
    elif project == 'raspberry-pi-lab':
        return render(request, 'raspberry-pi-lab.html')
    elif project == 'deep-learning-for-advanced-driver-assistance-system-applications':
        return render(request, 'deep-learning-for-advanced-driver-assistance-system-applications.html')
    elif project == 'open-webcam-test':
        return render(request, 'open-webcam-test.html')
    elif project == 'lottery':
        return lottery_view(request)
    elif project == 'exchange-rate':
        return exchange_rate_view(request)
    else:
        return render(request, '#')
    

def lottery_view(request):
    now = datetime.now()
    lottery_number = []

    for i in range(6):
        lottery_number.append(random.randrange(1, 46))

    lottery_number.sort()

    context = {
        "now_date": now.strftime('%Y-%m-%d %H:%M:%S'),
        "lottery_number": lottery_number,
    }

    return render(request, 'lottery.html', context)


SERVER_TIME = datetime.now()
UPDATE_DATE = ['01-01', '04-01', '07-01', '10-01']


class Fishingram(APIView):
    def get(self, request):

        '''
        
        낚시터 정보
        공공데이터포털 OPEN API
        
        '''
        
        open_api_url = 'https://openapi.gg.go.kr/FISHPLCINFO'
        params = {
            'KEY': '5ffbdad9c7384164869ac345484615b9',
            'TYPE': 'json',
            'pIndex': '1',
            'pSize': '300'
        }
        
        fishing_place_info_data = FishingPlaceInfoData.objects.all()
        serializer_class = FishingPlcInfoSerializer(fishing_place_info_data, many=True)

        #print(quary_setfishing_place_info_data)
        #print(valid_ckr)

        if (SERVER_TIME.strftime('%m-%d') in UPDATE_DATE):
            fishing_place_info_data.delete()

        valid_ckr = FishingPlaceInfoData.objects.count()

        if (valid_ckr == 0):
            req_data = requests.get(open_api_url, params)
            api_data = json.loads(req_data.text)

            if api_data['FISHPLCINFO'][0]['head'][1]['RESULT']['CODE'] != 'INFO-000':
                return render(request, "fishingram.html")

            total_cnt = api_data['FISHPLCINFO'][0]['head'][0]['list_total_count']

            for i in range(total_cnt):
                srl_data = {
                    'sigun_name': api_data['FISHPLCINFO'][1]['row'][i]['SIGUN_NM'],
                    'sigun_code': api_data['FISHPLCINFO'][1]['row'][i]['SIGUN_CD'],
                    'facility_name': api_data['FISHPLCINFO'][1]['row'][i]['FACLT_NM'],
                    'facility_type': api_data['FISHPLCINFO'][1]['row'][i]['FACLT_DIV_NM'],
                    'refine_roadnm_addr': api_data['FISHPLCINFO'][1]['row'][i]['REFINE_ROADNM_ADDR'],
                    'refine_lotnm_addr': api_data['FISHPLCINFO'][1]['row'][i]['REFINE_LOTNO_ADDR'],
                    'refine_lat': api_data['FISHPLCINFO'][1]['row'][i]['REFINE_WGS84_LAT'],
                    'refine_logt': api_data['FISHPLCINFO'][1]['row'][i]['REFINE_WGS84_LOGT'],
                    'facility_tel': api_data['FISHPLCINFO'][1]['row'][i]['FACLT_TELNO'],
                    'wtr_ar': api_data['FISHPLCINFO'][1]['row'][i]['WTR_AR'],
                    'fishkind_nm': api_data['FISHPLCINFO'][1]['row'][i]['FISHKIND_NM'],
                    'aceptnc_posbl_psn_cnt': api_data['FISHPLCINFO'][1]['row'][i]['ACEPTNC_POSBL_PSN_CNT'],
                    'wtr_facility_info': api_data['FISHPLCINFO'][1]['row'][i]['WTR_FACLT_INFO'],
                    'chrg_info': api_data['FISHPLCINFO'][1]['row'][i]['CHRG_INFO'],
                    'main_plc_info': api_data['FISHPLCINFO'][1]['row'][i]['MAIN_PLC_INFO'],
                    'safe_facility_info': api_data['FISHPLCINFO'][1]['row'][i]['SAFE_FACLT_INFO'],
                    'convnce_facility_info': api_data['FISHPLCINFO'][1]['row'][i]['CONVNCE_FACLT_INFO'],
                    'circumfr_tursm_info': api_data['FISHPLCINFO'][1]['row'][i]['CIRCUMFR_TURSM_INFO'],
                    'manage_inst_telno': api_data['FISHPLCINFO'][1]['row'][i]['MANAGE_INST_TELNO'],
                    'manage_inst_name': api_data['FISHPLCINFO'][1]['row'][i]['MANAGE_INST_NM'],
                    'data_std_de': api_data['FISHPLCINFO'][1]['row'][i]['DATA_STD_DE']
                }

                srz = FishingPlcInfoSerializer(data=srl_data)

                if srz.is_valid():
                    srz.save()

        tmp_data = json.dumps(serializer_class.data, ensure_ascii=False)

        context = {
            'fishing_place_info': tmp_data
        }

        #return JsonResponse(context)
        return render(request, "fishingram.html", context)


def exchange_rate_view(request):

    return render(request, 'exchange-rate.html')