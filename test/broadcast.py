import redis
channel='taskBroadcast'
r=redis.Redis(host='localhost',port=6379,db=0)
msg=r.pubsub()
msg.subscribe(channel)
while True:
    data=msg.parse_response()
    print data
