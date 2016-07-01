import redis

def func(p):
    open('/tmp/report.log','a').write(p["data"] + "\n----------------\n")

master = redis.Redis(host = '172.17.0.12',port = 6379)
psobj = master.pubsub()
psobj.subscribe(report=func)
L = psobj.listen()
L.get_messages()
for x in L:
    pass
