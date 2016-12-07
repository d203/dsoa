#-*- coding=utf-8 -*-
def req(self):
    def __init__ (self):
        self.requestId=''
        self.requestName=''
        self.requestTime=''
        self.paramList=''
        self.paramValue={}
    def getJson():
        reqDict={requestId,requestName,requestTime,paramList,paramValue}
        return json.dumps(reqDict)
    def setFromjson(jsonDict):
        self.requestId=jsonDict['requestId']
        self.requestName=jsonDict['requestName']
        self.requestTime=jsonDict['requestTime']
        self.paramList=jsonDict['paramList']
        self.paramValue=jsonDict['paramValue']
