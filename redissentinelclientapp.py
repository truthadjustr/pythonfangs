# -*- coding: utf-8 -*-
from optparse import OptionParser
import sys
import signal
import time
import datetime
import redis
import keygen
from redis.sentinel import Sentinel

def signal_handler(signal,frame):
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

try:
    parser = OptionParser()
    parser.add_option("-n",dest='numofkeys')
    (options,args) = parser.parse_args()

    if len(sys.argv) == 1:
        print('please suppply sentinel ipaddrs')
        sys.exit(1)

    sentinel = Sentinel(
        [(arg.split(':')[0],arg.split(':')[1]) for arg in args[1:]],
        socket_timeout = 0.5
    )
    print('detected master is %s' % str(sentinel.discover_master('mymaster')))
    time.sleep(5)
    master = sentinel.master_for('mymaster',socket_timeout = 0.1)
    #master = redis.StrictRedis(host='172.17.0.7') 
except:
    print(sys.exc_info()[0])
    sys.exit(1)

print("key insertion to commence in 3s ...")
time.sleep(3)

value = datetime.datetime.now()
key,value = keygen.generate_kv_pair()

num = int(options.numofkeys) if options.numofkeys else -1
count = 0
while count != num:
    try:
        print("[%s] setting %s -> %s [" % (datetime.datetime.now(),key,value)),
        master.set(key,value)
        print("✓]")
        value = datetime.datetime.now()
        # generate a test key/value pair
        count = count + 1
        key,value = keygen.generate_kv_pair()
    except: 
        # fail to insert key into redis
        print("x]")
    # our artificial delay
    time.sleep(0.2)

