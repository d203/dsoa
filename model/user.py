import json
from redisco import models
class User(models.Model):
    username=models.Attribute(required=True)
    createTime=models.DateTimeField(auto_now_add=True)
    password=models.Attribute(required=True)
    def get_json(self):
        return json.dumps({
            'username':self.username,
            'password':self.password
        })
