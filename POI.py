# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 11:14:19 2016

@author: hxw186


generate the POI count in each NTA
"""



import shapefile
from shapely.geometry import Polygon, Point, box
import numpy as np



def getNYC_NTA():
    
    fin = "../../dataset/nynta_14c/wgs84"
    
    ntas = {}
    sf = shapefile.Reader(fin)
    n = len(sf.shapes())
    
    for i in range(n):
        rcd = sf.record(i)
        shp = sf.shape(i)
        # only process Manhattan POI
        if rcd[3][:2] == "MN":
            nta_id = rcd[3]
            bndy = Polygon(shp.points)
            ntas[nta_id] = bndy
    assert len(ntas) == 29
    return ntas




def map_POI_to_NTA(ntas):
    
    pois = np.loadtxt("data/POI.csv", delimiter=",", skiprows=1)
    
    nta_poi = {}
    
    for row in pois:
        loc = Point(row[2], row[1])
        category = int(row[3])
        ucnt = int(row[4])
        for k, ply in ntas.items():
            if ply.contains(loc):
                if k in nta_poi:
                    if category in nta_poi[k]:
                        nta_poi[k][category] += ucnt
                    else:
                        nta_poi[k][category] = ucnt
                else:
                    nta_poi[k] = {}
                    nta_poi[k][category] = ucnt
                break

    for nta in nta_poi:
        sum_pois = sum(nta_poi[nta].values())
        for ctgk in nta_poi[nta]:
            nta_poi[nta][ctgk] /= float(sum_pois)
            
    assert sum(nta_poi['MN17'].values()) - 1 < 0.00000001
    return nta_poi
    



def output_NTA_POI(nta_poi):
    """There are 10 POI category in total"""
    
    with open("data/nta_poi.csv", 'w') as fout:
        # output NTA key
        ntas = nta_poi.keys()
        fout.write(",".join( ntas ) + "\n")
        for i in range(10):
            o = []
            for nta in nta_poi:
                if i not in nta_poi[nta]:
                    o.append('0')
                else:
                    o.append( str(nta_poi[nta][i]) )
            fout.write(",".join( o ) + "\n")


    
    

if __name__ == "__main__":
    
    s = getNYC_NTA()
    nta_poi = map_POI_to_NTA(s)
    output_NTA_POI(nta_poi)
    
                
    
    