# -*- coding: utf-8 -*-
import sys
import redis

arg = sys.argv[1].split(':')
ipaddr,port = arg[0],6379 if len(arg) == 1 else arg[1]
master = redis.StrictRedis(host=ipaddr,port=port) 

key,value = 'red','apple'
master.set(key,value)
