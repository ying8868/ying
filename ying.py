#!/usr/bin/python3 
import sys
from  lib.ying_init import *
from  lib.ying_quote import *
import config as conf

gq =get_quote(conf)

def Version():
    print ('leiying.py 1.0.0.0.1')

def main(argv):  
    Version()
         
 

if __name__ == '__main__':
    main(sys.argv)

