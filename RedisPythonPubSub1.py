import time
import redis
import threading

class Listener(threading.Thread):
    def __init__(self, r, channels):
        threading.Thread.__init__(self)
        self.redis = r
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
    
    def work(self, item):
        print item['channel'], ":", item['data']
    
    def run(self):
        for item in self.pubsub.listen():
            if item['channel'] == 'sys' and item['data'] == "KILL":
                self.pubsub.unsubscribe()
                print self, "unsubscribed and finished"
                break
            else:
                self.work(item) if not isinstance(item['data'],long) else None

if __name__ == "__main__":
    r = redis.Redis(host = '172.17.0.12')
    client = Listener(r, ['sys','weather','sports','business'])
    client.start()
    # time.sleep(5) 
    # r.publish('test', 'this will reach the listener')
    time.sleep(10) 
    r.publish('sys', 'KILL')
