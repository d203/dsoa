
import uuid as UUID
import json
from redisco import models
class Service(models.Model):
    name=models.Attribute(required=True)
    createdTime=models.DateTimeField(auto_now_add=True)
    IP=models.Attribute()
    uuid=models.Attribute()
    load=models.IntegerField()
    calcAbility=models.FloatField()

    def setFromjson(self,jsonDict):
        print jsonDict
        self.name=jsonDict['serviceName']
        self.IP=jsonDict['serviceIP']
        self.load=jsonDict['load']
        self.calcAbility=jsonDict['calcAbility']
    def setDebugger(self,debugger):
        self.debugger=debugger
        self.debugger(self.name+': debugger has been set')

    def run(self):
        self.uuid=str(UUID.uuid1())
        self.debugger('['+self.name+'] : service now add in service;\n   ip '+self.IP+'\n   uuid is: '+self.uuid)
    def get_json(self):
        return json.dumps({
                'serviceName':self.name,
                'serviceIP':self.IP,
                'serviceUUID':self.uuid
                })
