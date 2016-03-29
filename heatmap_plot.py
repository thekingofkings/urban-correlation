# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:14:19 2016

@author: hxw186


plot the heatmap of dropoff and pickup in different days.


2012-10-29 is the day Sandy landed NYC
2012-10-08
"""

from matplotlib import rcParams
import matplotlib.pyplot as plt
import pandas as pd


def plot_pickup_dropoff(fname = "2012-10-29"):
    df = pd.read_csv("data/{0}.csv".format(fname), header=None, names=['plon', 'plat', 'dlon', 'dlat'])
    
    
    rcParams["figure.figsize"] = (8, 6)
    plt.figure()
    ax = plt.subplot()
    ax.set_axis_bgcolor('black')
    
#    df = df.sample(frac=0.7)
    p = df.plot(kind='scatter', ax=ax, x='plon', y='plat', color='white', 
            xlim=(-74.05, -73.82), ylim=(40.68, 40.85), s=0.02, alpha=0.15)
            
    p.axes.get_xaxis().set_visible(False)
    p.axes.get_yaxis().set_visible(False)
    plt.savefig("fig/{0}-pickup.png".format(fname))
    
    
#    plt.figure()
#    ax2 = plt.subplot()
#    ax2.set_axis_bgcolor('black')
#    
#    p = df.plot(kind='scatter', ax=ax2, x='dlon', y='dlat', color='white', 
#            xlim=(-74.06, -73.77), ylim=(40.61, 40.91), s=0.02, alpha=0.6)
#            
#    p.axes.get_xaxis().set_visible(False)
#    p.axes.get_yaxis().set_visible(False)
#    plt.savefig("fig/{0}-dropoff.png".format(fname))
    
    
    
    
if __name__ == '__main__':
    # sandy
    plot_pickup_dropoff("2012-10-29")
    
    # chirstmas
    plot_pickup_dropoff("2012-12-25")
    
    # Saturday
#    plot_pickup_dropoff("2012-12-09")
    
    # Monday
    plot_pickup_dropoff("2012-12-10")