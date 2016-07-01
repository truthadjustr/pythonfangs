import sys
import random
import crcmod

crc16_func = crcmod.predefined.mkCrcFun('xmodem')
word_file = '/usr/share/dict/words'
WORDS = open(word_file).read().splitlines()

def generate_kv_pair():
    key = random.choice(WORDS)
    value = int(crc16_func(key))
    return key,value

if __name__ == '__main__':
    key = sys.argv[1] if len(sys.argv) > 1 else ""
    value = int(crc16_func(key))
    print("%s --> %d/%x ->%d" % (key,value,value,value % 16384))
