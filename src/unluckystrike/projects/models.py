from django.db import models

# Create your models here.

class Project(models.Model):
    pass


class FishingPlaceInfoData(models.Model):
    sigun_name = models.CharField(max_length=255)
    sigun_code = models.IntegerField(null=True)
    facility_name = models.CharField(max_length=255, null=True)
    facility_type = models.CharField(max_length=255, null=True)
    refine_roadnm_addr = models.CharField(max_length=255, null=True)
    refine_lotnm_addr = models.CharField(max_length=255, null=True)
    refine_lat = models.CharField(max_length=255, null=True)
    refine_logt = models.CharField(max_length=255, null=True)
    facility_tel = models.CharField(max_length=255, null=True)
    wtr_ar = models.CharField(max_length=255, null=True)
    fishkind_nm = models.CharField(max_length=255, null=True)
    aceptnc_posbl_psn_cnt = models.IntegerField(null=True)
    wtr_facility_info = models.CharField(max_length=255, null=True)
    chrg_info = models.CharField(max_length=255, null=True)
    main_plc_info = models.CharField(max_length=255, null=True)
    safe_facility_info = models.CharField(max_length=255, null=True)
    convnce_facility_info = models.CharField(max_length=255, null=True)
    circumfr_tursm_info = models.CharField(max_length=255, null=True)
    manage_inst_telno = models.CharField(max_length=255, null=True)
    manage_inst_name = models.CharField(max_length=255, null=True)
    data_std_de = models.CharField(max_length=255, null=True)