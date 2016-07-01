# -*- coding: utf-8 -*-
import sys
from optparse import OptionParser
import signal
import time
import datetime
import redis
import keygen

def signal_handler(signal,frame):
    print('was able to set %d keys' % count)
    sys.exit(0)

signal.signal(signal.SIGINT,signal_handler)

try:
    if len(sys.argv) == 1:
        print('please supply redis ipaddr')
        sys.exit(1)

    parser = OptionParser()
    parser.add_option('-n',dest='numofkeys')
    (options,args) = parser.parse_args()
    ipaddr = args[0].split(':')[0]
    port = int(args[0].split(':')[1])
    master = redis.StrictRedis(host=ipaddr,port=port) 
except:
    print(sys.exc_info()[0])
    sys.exit(1)

print("key insert to commence in 3s ...")
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
        key,value = keygen.generate_kv_pair()
        count = count + 1
    except: 
        # fail to insert key into redis
        print("x]")
    # our artificial delay
    time.sleep(0.2)
