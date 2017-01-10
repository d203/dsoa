import json
from redisco import models
class DataPackage(models.Model):
    package_name=models.Attribute(required=True)

class WorkerScript(models.Model):
    script_name=models.Attribute(required=True)
