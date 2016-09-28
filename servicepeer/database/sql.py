import os
import sqlite3
from flask import Flask,request,session,g,redirect,url_for,abort,\
    render_template,flash
app=Flask(__name__)
app.config['DATABASE']='./schema.sql'
def connect_db():
    rv=sqlite3.connect(app.config['DATABASE'])
    rv.row_factory=sqlite3.Row
    return rv

if __name__=='__main__':
    app.run()
