from django.db import models
from wokengineers.helpers.model_helpers import CommonModel, CustomUpdateManager
from wokengineers.helpers.model_helpers import add_log_model

# Create your models here.

class HeadLocationDetail(CommonModel):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    latitude = models.CharField(max_length=100, null=False)
    longitude = models.CharField(max_length=100, null=False)

    class Meta:
        abstract = True


class LocationDetail(HeadLocationDetail):
    CustomUpdateManager.set_logModel(logModel= "LocationDetailLog",  model= "LocationDetail")
    objects = CustomUpdateManager.as_manager()

    class Meta:
        db_table = "location_detail"

    def save(self, *args, **kwargs):
        super().save( *args, **kwargs)
        add_log_model(LocationDetailLog, self, "LocationDetailLog")


class LocationDetailLog(HeadLocationDetail):
    log = models.ForeignKey('LocationDetail',  on_delete=models.RESTRICT, null=False)
    updation_by = None
    updation_date = None

    class Meta:
        db_table = "location_detail_log"
