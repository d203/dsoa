import json
from redisco import models
class WorkerTask(models.Model):
    task_id=models.Attribute(required=True)
    worker_name=models.Attribute(required=True)
    script_code=models.Attribute(required=True)
    status=models.Attribute()
