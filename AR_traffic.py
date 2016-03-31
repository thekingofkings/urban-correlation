# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 22:39:29 2016

@author: hxw186


Use AutoRegressive Model to fit traffic (pickup/dropoff) time series.

"""

import numpy as np
import statsmodels.tsa.ar_model as ar
import statsmodels.tsa.arima_model as arima
import matplotlib.pyplot as plt





def plot_tsa_prediction(train_data, test_idx, test_data, predicted_res):
    """ use pyplot to visualize """
    
    plt.figure()
    plt.plot(train_data, 'b-')
    plt.plot(test_idx, test_data, 'b--')
    plt.plot(test_idx, predicted_res, 'r--')






if __name__ == '__main__':

    fn = "data/msg_Y.csv"
    jacobT = np.loadtxt(fn)
    n = 400 # jacobT.shape[0]
    
    train_idx = range(168)
    test_idx = range(168, n)
    
    jacob_d = jacobT[:,0]
    jacob_p = jacobT[:,1]
    
    train_d = jacob_d[train_idx]
    test_d = jacob_p[test_idx]
    
    arm = ar.AR(train_d)
    res = arm.fit(method="cmle", maxlag=48, ic="aic", trend="c")
    t = res.predict(168, n-1)
    
    
    plot_tsa_prediction(train_d, test_idx, test_d, t)



#    arma = arima.ARMA(train_d, order=(10,10))
#    res2 = arma.fit()
#    t2 = res2.predict(168, n-1)
#    
#    plot_tsa_prediction(train_d, test_idx, test_d, t2)