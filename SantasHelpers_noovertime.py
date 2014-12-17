__author__ = 'Alan Meert'
__date__ = 'December 7, 2014'

import os
import csv
import math
import heapq
import time
import datetime
import numpy as np
from collections import OrderedDict
from bisect import bisect_left

from hours import Hours
from toy import Toy
from elf import Elf
from SantasHelpers_NaiveSolution import assign_elf_to_toy

def create_elves(NUM_ELVES):
    """ Elves are stored in a sorted list using heapq to maintain their order by next available time.
    List elements are a tuple of (next_available_time, elf object)
    :return: list of elves
    """
    list_elves = []
    for i in xrange(1, NUM_ELVES+1):
        list_elves.append(Elf(i))
    return list_elves

def solution_noovertime(toy_file, soln_file, myelves):
    """ Creates a simple solution where the next available elf is assigned a toy. Elves do not start
    work outside of sanctioned hours.
    :param toy_file: filename for toys file (input)
    :param soln_file: filename for solution file (output)
    :param myelves: list of elves in a priority queue ordered by next available time
    :return:
    """
    hrs = Hours()
    ref_time = datetime.datetime(2014, 1, 1, 0, 0)
    row_count = 0
    with open(toy_file, 'rb') as f:
        toysfile = csv.reader(f)
        toysfile.next()  # header row

        available_toys = OrderedDict([])

        for row in toysfile:
            available_toys[row[0]]=Toy(row[0], row[1], row[2])
            

    with open(soln_file, 'wb') as w:
        wcsv = csv.writer(w)
        wcsv.writerow(['ToyId', 'ElfId', 'StartTime', 'Duration'])
    

        toys_assigned = [9999,]
        start_times = np.array([a.next_available_time for a in myelves])
        while len(available_toys.keys())>0:
            print 'available_toys ', len(available_toys.keys())
            tot_ass = 0
            to_pop =[]
            for toycount, currtoy in available_toys.items():
                best_times2 = np.where(currtoy.arrival_minute>=start_times, np.nan, start_times)
                best_times = np.argsort(best_times2)
                    
                for elfpos in best_times:
                    try:
                        work_start_time = int(best_times2[elfpos])
                    except ValueError:
                        break
                    current_elf = myelves[elfpos]
                # work_start_time cannot be before toy's arrival
                #if work_start_time < current_toy.arrival_minute:
                #    print 'Work_start_time before arrival minute: {0}, {1}'.\
                #        format(work_start_time, current_toy.arrival_minute)
                #    exit(-1)

                    next_available_time, work_duration, unsanctioned = \
                        assign_elf_to_toy(work_start_time, current_elf, currtoy, hrs)
                    
                    if (unsanctioned == 0 or toys_assigned[-1]==0 or current_elf.rating>3.5):
                        current_elf.next_available_time = next_available_time
                        current_elf.update_elf(hrs, currtoy, work_start_time, work_duration)
                        start_times[elfpos]=current_elf.next_available_time
                # write to file in correct format
                        tt = ref_time + datetime.timedelta(seconds=60*work_start_time)
                        time_string = " ".join([str(tt.year), str(tt.month), str(tt.day), str(tt.hour), str(tt.minute)])
                        wcsv.writerow([currtoy.id, current_elf.id, time_string, work_duration])
                                                
                        tot_ass+=1
                        del available_toys[toycount]
                        break
            toys_assigned.append(tot_ass)
            print 'productivities'
            print [a.rating for a in myelves]

        print toys_assigned
        return

if __name__ == '__main__':

    for count in [200, ]:
        start = time.time()
        NUM_ELVES = count
        myelves = create_elves(NUM_ELVES)


        for month in range(1,13):
            print "month ", month
#        toy_file = os.path.join(os.getcwd(), 'data/test_toys.csv')
#        soln_file = os.path.join(os.getcwd(), 'data/noovertime2_test_%d.csv' %count)
            toy_file = os.path.join(os.getcwd(), 'data/toys_%d.csv' %month)
            soln_file = os.path.join(os.getcwd(), 'data/noovertime2_%d_m%d.csv' %(count, month))

            solution_noovertime(toy_file, soln_file, myelves)

            print 'total runtime = {0}'.format(time.time() - start)
