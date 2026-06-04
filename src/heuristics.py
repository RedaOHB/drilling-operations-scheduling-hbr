import numpy as np
import pandas as pd
import random
from utils import Time  # import helper function    


"""
  nearest_neighbor(travel_time, drilling, M)

  implements Nearest Neighbor heuristic 

  # Parameters: 

   - `travel_time`: travel time between wells for each device (DataFrame)
   - `drilling`: drilling time required for each well  (DataFrame)
   - `M`: number of devices  (int)

  # Result:

   - `displacements`: routing sequence for each device
   - `Total_time`: total time required to complete the drilling of all wells
"""

def nearest_neighbor(travel_time, drilling, M):

    # convert the DataFrame to a NumPy array for further processing
    devices_travel_time = travel_time.to_numpy()  
    well_drilling_time = drilling.to_numpy()  
    # remove the column containing the well names
    devices_travel_time = devices_travel_time[:,1:] 
    well_drilling_time = well_drilling_time[:,1]  


    N = len(devices_travel_time) - 1 # number of wells

    # constructs the sets of all wells and devices
    Wells = []  # set of wells
    Devices = []  # set of devices

    for i in range(1,N+1): 
        Wells.append(i)   
    for k in range(1, M+1):
        Devices.append(k)

    displacements = [[0] for _ in range(M)]  # vector representing the movement of each device from one well to another
    drilling_time = np.zeros(M)  # vector containing the drilling time for each device

    # select the M wells closest to the depot
    index = np.argsort(devices_travel_time[0, :])  # sort the wells from closest to farthest in terms of travel time
    for i in range(1,M+1): 
        displacements[i-1].append(int(index[i]))  # assign the M devices to the M wells closest to the depot
        Wells.remove(index[i])  # remove wells that have already been drilled from the list or set
        for j in range(N+1):  # set travel time to infinity between the newly added well and all other wells
            devices_travel_time[j][int(index[i])] = 1000

    # set the travel time between each well and itself to infinity
    for j in range(N+1):
        devices_travel_time[j][j] = 1000  
        devices_travel_time[j][0] = 1000  # travel time between each well and the depot

    while len(Wells) >= M:             
        for k in range(M):
            j = len(displacements[k])  # select the last well drilled by device k
            x = np.argmin(devices_travel_time[int(displacements[k][j-1])])  # select the closest well
            displacements[k].append(int(x))  # add the selected well to the current drilling sequence
            Wells.remove(int(x))  # remove the selected well from the set of available wells
            for i in range(N+1):
                devices_travel_time[i][x] = 1000  

    while len(Wells) >= 1:
        k = random.randrange(0, M)   # select a device randomly
        j = len(displacements[k])  # select the last well drilled by device k
        x = np.argmin(devices_travel_time[int(displacements[k][j-1])]) # select the closest well
        displacements[k].append(int(x))  # add the selected well to the current drilling sequence 
        Wells.remove(int(x))  # remove the selected well from the set of available wells
        for i in range(N+1):  
                devices_travel_time[i][x] = 1000

    drilling_time = Time(displacements, devices_travel_time, well_drilling_time)  # drilling time for each device
    
    Total_time = np.max(drilling_time)   # total drilling time      
    
    return displacements, Total_time



"""
  insertion(travel_time, drilling, M)

  implements insertion heuristic 

  # Parameters: 

   - `travel_time`: travel time between wells for each device (DataFrame)
   - `drilling`: drilling time required for each well  (DataFrame)
   - `M`: number of devices  (int)

  # Result:

   - `displacements`: routing sequence for each device
   - `Total_time`: total time required to complete the drilling of all wells
"""

def insertion(travel_time, drilling, M):

    # convert the DataFrame to a NumPy array for further processing
    devices_travel_time = travel_time.to_numpy()  
    well_drilling_time = drilling.to_numpy()  
    # remove the column containing the well names
    devices_travel_time = devices_travel_time[:,1:] 
    well_drilling_time = well_drilling_time[:,1]  

    T = np.copy(devices_travel_time)  # copy the travel_time matrix

    N = len(devices_travel_time) - 1  # number of wells

    # constructs the sets of all wells and devices
    Wells = []  # set of wells
    Devices = []  # set of devices

    for i in range(1,N+1): 
        Wells.append(i)   
    for k in range(1, M+1):
        Devices.append(k)

    displacements = [[0] for _ in range(M)]  # vector representing the movement of each device from one well to another
    drilling_time = np.zeros(M)  # vector containing the drilling time for each device

    # select the M wells closest to the depot
    index = np.argsort(devices_travel_time[0, :])  # sort the wells from closest to farthest in terms of travel time
    for k in range(1,M+1): 
        displacements[k-1].append(int(index[k]))  # assign the M devices to the M wells closest to the depot
        Wells.remove(index[k])  # remove wells that have already been drilled from the list or set
        for i in range(N+1):  # set travel time to infinity between the newly added well and all other wells
            devices_travel_time[i][int(index[k])] = 1000

    # set the travel time between each well and itself to infinity
    for i in range(N+1):
        devices_travel_time[i][i] = 1000  
        devices_travel_time[i][0] = 1000  # travel time between each well and the depot

    
    while len(Wells) >= M:
        for k in range(M):
            # construct the travel time matrix between resting and drilling wells for each device
            D=[]
            for j in displacements[k]:
                if (j != 0):
                   D.append(j)
            P = Wells 

            Matrix = devices_travel_time[np.ix_(D, P)]
            min_index = np.unravel_index(np.argmin(Matrix), Matrix.shape)  # find the coordinates of the closest well to the current cycle
            z1 = displacements[k][int(min_index[0])+1]    
            z2 = P[min_index[1]]

            # find the best position to insert the selected well into the cycle
            if (min_index[0] == 0):
               displacements[k].insert(min_index[0]+2 , z2)  
            else:
                S1 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]-1]] + devices_travel_time[displacements[k][min_index[0]-1]][displacements[k][min_index[0]]]
                S2 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]+1]] + devices_travel_time[displacements[k][min_index[0]+1]][displacements[k][min_index[0]]]
                if (S1 < S2):
                    displacements[k].insert(min_index[0]+1, z2)
                else:
                    displacements[k].insert(min_index[0]+2, z2)

            Wells.remove(z2)  # remove the inserted well

            # set the travel time between well "z2" and all other wells to infinity
            for i in range(N+1):
                devices_travel_time[i][z2] = 1000
        
    
    while (len(Wells) >= 1):
        k = random.randrange(0, M) # select a device randomly
        # construct the travel time matrix between resting and drilling wells for each device
        D=[]
        for j in displacements[k]:
            if (j != 0):
               D.append(j)
        P = Wells 

        Matrix = devices_travel_time[np.ix_(D, P)]
        min_index = np.unravel_index(np.argmin(Matrix), Matrix.shape)  # find the coordinates of the closest well to the current cycle
        z1 = displacements[k][int(min_index[0])+1]
        z2 = P[min_index[1]]

        # find the best position to insert selected well in the cycle
        if (min_index[0] == 0):
           displacements[k].insert(min_index[0]+2 , z2)
        else:
            S1 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]-1]] + devices_travel_time[displacements[k][min_index[0]-1]][displacements[k][min_index[0]]]
            S2 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]+1]] + devices_travel_time[displacements[k][min_index[0]+1]][displacements[k][min_index[0]]]
            if (S1 < S2):
                displacements[k].insert(min_index[0]+1, z2)
            else:
                displacements[k].insert(min_index[0]+2, z2)

        Wells.remove(z2)  # remove the inserted well  

        # set the travel time between well "z2" and other wells to infinity
        for i in range(N+1):
            devices_travel_time[i][z2] = 1000
        

    drilling_time = Time(displacements, T, well_drilling_time)  # drilling time for each device

    Total_time = np.max(drilling_time)  # total drilling time

    return displacements, Total_time
    
