# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 10:16:00 2016

@author: fxw133
"""

import numpy   as np
import time
import datetime

# functions for pre_processing data
# (t,x,y,v) --> (t,v'): v'-> agg(X,Y,X,T)
#
# bounding boxes
location = {}
location['jacob']      = (np.array([-74.004524231,40.7548644534]),np.array([-73.9958113432,40.7593078613])) # (lower-left), (upper-right)
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
    return np.where(np.logical_and(timestamps < timeu, timestamps >= timel))
    
def within_timeframe(timestamp, timeframe):
    return (timestamp >= timeframe[0]) and (timestamp <= timeframe[1]) 

def get_data_within_box_timeframe(context_data, target_location, time_frame):
    # IN:  context data {'samplenames':[samples]}
    #      target_loction (np.array([# upper-right point]),np.array([# lower-left point])) 
    # OUT: filtered_context_data {'samplenames':[samples]}
    filtered_context_data = dict()
    n_data = context_data.keys()
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
            d          = np.sum(time_index)
        else:
            d          = np.sum(samples[time_index,count_index])
        ts.append(d)
        start_ts.append(t_p1)
        t_p1       = t_p2
        t_p2       = t_p1 + time_step
    return np.array(ts), start_ts
    
def expand_by_period(ts, K):
    # expand time seris of a week to target time span
    return ts.tolist()*K
    
    
### dataset specific pre-processing
    
    
    

    

    
    