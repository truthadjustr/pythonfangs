# -*- coding: utf-8 -*-
from optparse import OptionParser
import sys
import signal
import time
import datetime
import keygen
from rediscluster import StrictRedisCluster

count = 0
parser = OptionParser()
parser.add_option("-n","--numofkeys",dest='numofkeys')

(options, args) = parser.parse_args()

def signal_handler(signal,frame):
    print("\nwas able to set %d keys" % count)
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

if len(sys.argv) == 1:
    print("./%s ipaddr1 ipaddr2 ipaddr3 [...]" % sys.argv[0])
    sys.exit(1)

try:
    '''
    startup_nodes = [
        {'host':'172.17.0.4','port':'6379'},
        {'host':'172.17.0.3','port':'6379'},
        {'host':'172.17.0.2','port':'6379'}
    ]
    '''

    startup_nodes = [{'host':'%s' % arg.split(':')[0],'port':'%s' % arg.split(':')[1]} for arg in args]
    cluster = StrictRedisCluster(startup_nodes = startup_nodes,decode_responses = True)
    #master = redis.StrictRedis(host='172.17.0.7') 
except:
    print(sys.exc_info()[0])
    sys.exit(1)

print("commencing SET operations in 3s ...")
time.sleep(3)

count = 0
num = int(options.numofkeys) if options.numofkeys else -1
key,value = keygen.generate_kv_pair()
while count != num:
    try:
        print("[%s] setting %s -> %s [" % (datetime.datetime.now(),key,value)),
        cluster.set(key,value)
        print("✓]")
        count = count + 1
        key,value = keygen.generate_kv_pair()
    except: 
        print("x]")
    time.sleep(0.1)
