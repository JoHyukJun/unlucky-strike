# fishingram

from rest_framework import serializers

from projects.models import FishingPlaceInfoData

import os
import glob

from pathlib import Path

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


class FishingPlcInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FishingPlaceInfoData
        fields = (
            'sigun_name',
            'sigun_code',
            'facility_name',
            'facility_type',
            'refine_roadnm_addr',
            'refine_lotnm_addr',
            'refine_lat',
            'refine_logt',
            'facility_tel',
            'wtr_ar',
            'fishkind_nm',
            'aceptnc_posbl_psn_cnt',
            'wtr_facility_info',
            'chrg_info',
            'main_plc_info',
            'safe_facility_info',
            'convnce_facility_info',
            'circumfr_tursm_info',
            'manage_inst_telno',
            'manage_inst_name',
            'data_std_de'
        )