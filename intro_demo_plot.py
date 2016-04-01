# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 15:38:03 2016

@author: hxw186


Plot synthetic traffic on map
"""


import matplotlib.pyplot as plt
import numpy.random as rnd


plt.figure(figsize=(16,12))
im = plt.imread("data/road-example.PNG")
implot = plt.imshow(im)
plt.box(on=False)

f = plt.gca()
f.axes.get_xaxis().set_visible(False)
f.axes.get_yaxis().set_visible(False)

plt.savefig("fig/intro-demo-base.png", bbox_inches='tight', pad_inches=0)

cov = [[11000, 4000], [8000, 12000]]
cov2 = [[3000,0], [0, 6000]]
cov3 = [[500,200], [200, 1000]]
pnts = rnd.multivariate_normal([1000, 450], cov, 2000)
pt2 = rnd.multivariate_normal([500, 600], cov2, 500)
pt3 = rnd.multivariate_normal([200, 200], cov3, 200)

plt.scatter(pnts[:,0], pnts[:,1], c='r', alpha=0.3)
plt.scatter(pt2[:,0], pt2[:,1], c='r', alpha=0.3)
plt.scatter(pt3[:,0], pt3[:,1], c="r", alpha=0.3)



plt.savefig("fig/intro-demo-traffic.png", bbox_inches='tight', pad_inches=0)