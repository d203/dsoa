from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
import os
import json
from Service import Service

app=Flask (__name__)

@app.route('/requestTask',methods=['POST'])
def requestTask():
    app.logger.debug(request.get_json()['data'])
    return ''

@app.route('/addService',methods=['POST'])
def addService():
    info=request.json
    print info
    service=Service()
    service.setFromjson(info)
    service.setDebugger(app.logger.debug)
    service.run()
    print service.save()
    return service.get_json()

@app.route('/')
def show_list():
    entries=db.get_entries()
    for e in entries:
        print 'title is:' +e.title+' text is:' +e.row+'/n'
if __name__=='__main__':
    app.debug=True
    app.run(port=8080)
