import json
from redisco import models
class DataPackage(models.Model):
    package_name=models.Attribute(required=True)
    def get_json(self):
        return json.dumps({
            'package_name':self.package_name
        })

class WorkerScript(models.Model):
    script_name=models.Attribute(required=True)
    def get_json(self):
        return json.dumps({
            'script_name':self.script_name
        })
