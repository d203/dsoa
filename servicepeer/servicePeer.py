from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
import os
import json

app=Flask(__name__)

@app.route('/requestTask',methods=['POST'])
def requestTask():
    app.logger.debug(request.get_json()['data'])

    return ''

@app.route('/')
def show_entries():
    entries=db.get_entries()
    for e in entries:
        print 'title is:' +e.title+' text is:' +e.row+'/n'
if __name__=='__main__':
    app.debug=True
    app.run(port=8080)
