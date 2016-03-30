"""

Author:Hongjian
Date:Mar 29, 2016


Find two region with opposite taxi pickup/dropoff pattern.
"""


from POI import getNYC_NTA
from shapely.geometry import Point
import matplotlib.pyplot as plt



def generate_taxi_trip_time_seiries(fin):
    NTAs = getNYC_NTA()
    
    
    ntas = {}
    
    with open(fin, 'r') as fin1:
        for line in fin1:
            ls = line.split(",")
            try:
                loc = Point(float(ls[1]), float(ls[2]))
            except ValueError:
                continue
            
            for k, nta in NTAs.items():
                if nta.contains(loc):
                    time_key = ls[0][11:13]
                    if k in ntas:
                        if time_key in ntas[k]:
                            ntas[k][time_key] += 1
                        else:
                            ntas[k][time_key] = 0
                    else:
                        ntas[k] = {}
                        ntas[k][time_key] = 1
    
    return ntas
        
        
        


def visualize_all_TS(nta_pickups, nta_dropoffs):
    """ plot the time series of pickup/dropoff of all NTA """
    i = 1
    plt.figure(figsize=(20, 15))
    for nta in nta_pickups:
        times = nta_pickups[nta].keys()
        sorted_time = sorted(times)
        traff_p = [nta_pickups[nta][T] for T in sorted_time]
        traff_d = [nta_dropoffs[nta][T] for T in sorted_time]
        
        plt.subplot(5,6,i)
        plt.plot(traff_p, 'r-')
        plt.plot(traff_d, 'b:')
        plt.title(nta)

        i += 1
    plt.show()
    






def visualize_special_case( nta_pickups, nta_dropoffs, ntas=["MN32", "MN17"] ):
    """ MN32 and MN17 are significantly different) """
    times = nta_pickups[ntas[0]].keys()
    sorted_time = sorted(times)
    
    plt.figure(figsize=(16,6))
    
    n = len(ntas)
    for i in range(n):
        f = plt.subplot(1,n,i)
        
        pkps = [nta_pickups[ntas[i]][T] for T in sorted_time]
        plt.plot(pkps, "r-", lw=4)
        
        dpfs = [nta_dropoffs[ntas[i]][T] for T in sorted_time]
        plt.plot(dpfs, "b--", lw=4)
        
        plt.legend(["Pickup", "Drop-off"], fontsize=18, loc='best')
        plt.xlabel("Hour of Monday 12/10/2012", fontsize=18)
        plt.ylabel("Traffic count of NTA #{0}".format(ntas[i]), fontsize=18)
        f.tick_params(axis='both', which='major', labelsize=16)
        f.tick_params(axis='both', which='minor', labelsize=12)
        
    plt.savefig("fig/two-nta-ts.pdf")
    



if __name__ == "__main__":
    
    
#    nta_pickups = generate_taxi_trip_time_seiries("data/2012-12-10-pick.csv")
#    nta_dropoffs = generate_taxi_trip_time_seiries("data/2012-12-10-drop.csv")
    
    visualize_all_TS(nta_pickups, nta_dropoffs)
    visualize_special_case(nta_pickups, nta_dropoffs)