import json
from redisco import models
class WorkerTask(models.Model):
    task_id=models.Attribute(required=True)
    worker_name=models.Attribute(required=True)
    script_code=models.Attribute(required=True)
    status=models.Attribute()
    file_package=models.Attribute()
    def get_json(self):
        return json.dumps({
            'task_id':self.task_id,
            'worker_name':self.worker_name,
            'script_code':self.script_code,
            'status':self.status,
            'file_package':self.file_package
        })
