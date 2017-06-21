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
    Avarage data in 10 seconds
    '''
    tmp = []
    avg = 0
    counter = 0
    for itm in data:
        avg += itm
        counter += 1
        if counter == 10:
            tmp.append(byte_to_mega(avg/10))
            avg = 0
            counter = 0
    if counter != 0:
        tmp.append(byte_to_mega(avg/counter))
    return tmp

def minute_average_noconvert(data):
    '''
    Avarage data in 1 minute
    '''
    tmp = []
    avg = 0
    counter = 0
    for itm in data:
        avg += itm
        counter += 1
        if counter == 10:
            tmp.append(avg/10)
            avg = 0
            counter = 0
    if counter != 0:
        tmp.append(avg/counter)
    return tmp

'''
Matplotlib color code 'k' = black
'''

def plot_cpu(usr, sys, idl, wai, filename):
    plt.figure()
    plt.plot(usr, label='CPU Usage', linestyle = '-', color = 'k')
    plt.plot(sys, label='CPU System', linestyle = '--', color = 'k')
    plt.plot(idl, label='CPU Idle', linestyle = '-.', color = 'k')
    plt.plot(wai, label='CPU Wait', linestyle = ':', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('CPU usage(%)')
    plt.title('CPU usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'cpu.pdf')

def plot_memory(usd, buf, cach, free, filename):
    plt.figure()
    plt.plot(usd, label='Memory Usaged', linestyle = '-', color = 'k')
    plt.plot(buf, label='Memory Buffer', linestyle = '--', color = 'k')
    plt.plot(cach, label='Memory Cache', linestyle = '-.', color = 'k')
    plt.plot(free, label='Memory Free', linestyle = ':', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('Memory usage(MB)')
    plt.title('Memory usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'memory.pdf')

def plot_disk(read, writ, filename):
    plt.figure()
    plt.plot(read, label='Disk Read', linestyle = '-', color = 'k')
    plt.plot(writ, label='Disk Write', linestyle = '--', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('Storage speed(MB)')
    plt.title('Storage usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'disk.pdf')

def plot_network(send, recv, filename):
    plt.figure()
    plt.plot(send, label='Network Send', linestyle = '-', color = 'k')
    plt.plot(recv, label='Network Receive', linestyle = '--', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('Network speed(MB)')
    plt.title('Network usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'net.pdf')

def plot_swap(usd, fre, filename):
    plt.figure()
    plt.plot(usd, label='Used', linestyle = '-', color = 'k')
    plt.plot(fre, label='Free', linestyle = '--', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('Size(MB)')
    plt.title('Swap memory usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'swap.pdf')

def plot_paging(i, o, filename):
    plt.figure()
    plt.plot(i, label='In', linestyle = '-', color = 'k')
    plt.plot(o, label='Out', linestyle = '--', color = 'k')
    plt.xlabel('10 Second(s)')
    plt.ylabel('Speed(MB)')
    plt.title('Paging usage')
    plt.legend()
    plt.savefig('/data/graph/'+filename+'page.pdf')

def main():
    '''
    Main function
    Argument [1]: File path
    '''
    if sys.argv[1] is None:
        print('No arguments')
        return 0
    file = str(sys.argv[1])
    filename = file.split('.')[0]
    data = pd.read_csv('/data/prepData/'+file, header=[0, 1])
    plot_cpu(minute_average_noconvert(data[('total cpu usage','usr')]), minute_average_noconvert(data[('total cpu usage','sys')]), minute_average_noconvert(data[('total cpu usage','idl')]), minute_average_noconvert(data[('total cpu usage','wai')]), filename)
    plot_memory(minute_average(data[('memory usage','used')]), minute_average(data[('memory usage','buff')]), minute_average(data[('memory usage','cach')]), minute_average(data[('memory usage','free')]), filename)
    plot_disk(minute_average(data[('dsk/total','read')]), minute_average(data[('dsk/total','writ')]), filename)
    plot_network(minute_average(data[('net/total','recv')]), minute_average(data[('net/total','send')]), filename)
    plot_swap(minute_average(data[('swap','used')]), minute_average(data[('swap','free')]), filename)
    plot_paging(minute_average(data[('paging','in')]), minute_average(data[('paging','out')]), filename)
    #d1 = [byte_to_mega(x) for x in data[('dsk/total', 'read')]]
    #d1 = minute_average(data[('dsk/total','read')])
    #d2 = minute_average(data[('dsk/total','writ')])
    #plt.plot(d1, label='Disk Read')
    #plt.plot(d2, label='Disk Write')
    #plt.savefig('/data/graph/'+filename+'.pdf')

if __name__ == '__main__':
    main()
