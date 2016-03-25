# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:16:00 2016

@author: fxw133
"""

import numpy   as np
import time
import datetime
import cPickle as pickle
import csv

# functions for pre_processing data
# (t,x,y,v) --> (t,v'): v'-> agg(X,Y,X,T)
#
# bounding boxes
location = {}
# location['jacob']      = (np.array([-74.004524231,40.7548644534]),np.array([-73.9958113432,40.7593078613])) # (lower-left), (upper-right)
location['jacob']      = (np.array([-74.0014117956, 40.7574610417]),np.array([-73.9997595549,40.7587369494])) #small box
location['timesquare'] = (np.array([-73.986483,40.759139]),np.array([-73.979144,40.763934]))
location['msg']        = (np.array([-73.996235,40.7482]),np.array([-73.990173,40.75213]))
# *location['58E']        = (np.array([-73.9733,40.756792]),np.array([-73.956922,40.764575]))
# *location['59E']        = (np.array([-73.97566,40.761398]),np.array([-73.968329,40.76555]))
# *location['mahattan']   = (np.array([-74.038646,40.69005]),np.array([-73.888142,40.902056]))

def date2linux_timestamp(s, time_format = '%m/%d/%Y'):
    ts = time.mktime(datetime.datetime.strptime(s,time_format).timetuple())
    return ts
    
def get_index_within_box(points, ur, ll):
    return np.all(np.logical_and(points <= ur, points >= ll), axis = 1)
    
def get_index_within_timeframe(timestamps, timel, timeu):
    return np.where(np.logical_and(timestamps < timeu, timestamps >= timel))[0]
    
def within_timeframe(timestamp, timeframe):
    return (timestamp >= timeframe[0]) and (timestamp <= timeframe[1]) 

def get_data_within_box_timeframe(context_data, target_location, time_frame):
    # IN:  context data {'samplenames':[samples]}
    #      target_loction (np.array([# upper-right point]),np.array([# lower-left point])) 
    # OUT: filtered_context_data {'samplenames':[samples]}
    filtered_context_data = dict()
    n_data                = context_data.keys()
    for one_type in n_data:
        kept_index_space                = get_index_within_box(context_data[one_type][:,1:3], target_location[0],target_location[1])
        kept_index_time                 = get_index_within_timeframe(context_data[one_type][:,0], time_frame[0], time_frame[1])
        kept_index                      = np.logical_and(kept_index_space, kept_index_time)
        filtered_context_data[one_type] = context_data[one_type][kept_index,:]
    return filtered_context_data
   
  
def aggregate_by_time(samples, time_frame, time_step, count_index = None):
    # samples are [[timestamp, lat,lon, value]...]
    # time_step is in seconds
    t_p1 = time_frame[0]
    t_p2 = t_p1  + time_step  
    ts       = list()
    start_ts = list()
    while t_p2 <= time_frame[1]:
        time_index = get_index_within_timeframe(samples[:,0], t_p1, t_p2)
        if count_index == None:
            d          = len(time_index)
        else:
            d          = np.sum(samples[time_index,count_index])
        ts.append(d)
        start_ts.append(t_p1)
        t_p1       = t_p2
        t_p2       = t_p1 + time_step
    return np.array(ts), start_ts
    
def expand_by_period(ts, K):
    # expand time seris of a week to target time span
    return ts*K
    
def prepare_poi_ts(poi_ts):
    new_ts_c = dict()    
    for one_cat in poi_ts:
        N         = np.sum(poi_ts[one_cat])
        new_ts    = [v[0]/float(N) for v in poi_ts[one_cat]]
        cat_index = one_cat
        new_ts_c[cat_index] = new_ts
    return new_ts_c
    
    
def load_set_data(context_names,file_ext,PATH2_PROCESSED_DATA):    
    context_data          = dict()
    for one_type in context_names:
        data_file_name = '{}{}.csv'.format(one_type, file_ext)
        print PATH2_PROCESSED_DATA.format(data_file_name)
        context_data[one_type]   = np.loadtxt(PATH2_PROCESSED_DATA.format(data_file_name), delimiter= ',')
    return context_data
    
    
### dataset specific pre-processing, raw_data processing
def extract_data_within_tl(PATH2CSV, timeframe, location_box, fields= ['timestamp','lon','lat'], time_format=None):
    result_csv = list()
    count      = 0
    with open(PATH2CSV) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if count % 10000 == 0 :
                print count
            count += 1
            one_row = [row[x] for x in fields]
            if time_format != None:
                one_row[0] = date2linux_timestamp(one_row[0], time_format)
            one_row = [float(x) for x in one_row]
            if within_timeframe(one_row[0], timeframe):
                result_csv.append(one_row)   
    dd = np.array(result_csv)
    box_index = get_index_within_box(dd[:,1:3], location_box[1], location_box[0])
    return dd[box_index,:]
    
# pre-processing 


def Something():
    PATH2_POI_TS         =  'C:\\Users\\fxw133\\Desktop\\super_correlation\\context_data\\processed_csv\\poi_ts.pickle'
    PATH2_PROCESSED_DATA =  'C:\\Users\\fxw133\\Desktop\\super_correlation\\context_data\\processed_csv\\{}'
    DATE_PREFIX          =  'OCT12\\{}'
    
    
    poi_ts        = prepare_poi_ts(pickle.load(open(PATH2_POI_TS,'r')))    # a time seris by hour
    
    file_ext      = 'jacob'
    taxi_data     = ['taxi_drop_','taxi_pick_']
    
    time_frame = (date2linux_timestamp('10/1/2012'),date2linux_timestamp('11/1/2012'))
    loaded_taxi_data = load_set_data(taxi_data, file_ext, PATH2_PROCESSED_DATA.format(DATE_PREFIX))
    
    ts_data    = dict()
    for a in taxi_data:
        ts_data[a], tsl = aggregate_by_time(loaded_taxi_data[a],time_frame, 3600, None)
        
    pickle.dump(ts_data, open('taxi_ts{}.pickle'.format(file_ext),'w'))
    





    

    
    