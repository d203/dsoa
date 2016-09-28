import requests
from test import count_words_at_url
from redis import Redis
import time
from rq import Queue,use_connection
if __name__=='__main__':
    use_connection()
    q=Queue(connection=Redis())
    url='http://www.baidu.com'
    for i in range(1,5):
        print 'The '+ str(i) +' task start'
