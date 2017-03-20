#!/usr/bin/env python3

import sys
import pandas as pd
import matplotlib.pyplot as plt

KILO = 1024.0
MEGA = 1048576.0
GIGA = 1073741824.0

def byte_to_mega(num):
    '''
    Convert byte to megabyte
    '''
    return float("{0:.2f}".format(num/MEGA))

def minute_average(data):
    '''
    Avarage data in 1 minute
    '''
    tmp = []
    avg = 0
    counter = 0
    for itm in data:
        avg += itm
        counter += 1
        if counter == 60:
            tmp.append(byte_to_mega(avg/60))
            avg = 0
            counter = 0
    if counter != 0:
        tmp.append(byte_to_mega(avg/counter))
    return tmp

def main():
    '''
    Main function
    '''
    if sys.argv[1] is None:
        print('No arguments')
        return 0
    file = str(sys.argv[1])
    filename = file.split('.')[0]
    data = pd.read_csv('/data/prepData/'+file, header=[0, 1])
    #d1 = [byte_to_mega(x) for x in data[('dsk/total', 'read')]]
    d1 = minute_average(data[('dsk/total','read')])
    d2 = minute_average(data[('dsk/total','writ')])
    plt.plot(d1)
    plt.plot(d2)
    plt.savefig('/data/graph/'+filename+'.pdf')

if __name__ == '__main__':
    main()
