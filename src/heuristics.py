import numpy as np
import pandas as pd
import random



def nearest_neighbor(travel_time, drilling, M):

    devices_travel_time = travel_time.to_numpy()  # convert the DataFrame to a NumPy array for further processing
    devices_travel_time = devices_travel_time[:,1:]  # remove the column containing the well names
    well_drilling_time = drilling.to_numpy()  
    well_drilling_time = well_drilling_time[:,1]  


    N = len(devices_travel_time) - 1 # number of wells


    # constructs the set of all wells and devices
    Wells = []  # wells set
    Devices = []  # devices set

    for i in range(1,N+1): 
        Wells.append(i)   
    for k in range(1, M+1):
        Devices.append(k)

    displacements = [[0] for _ in range(M)]  # a vector containing the movement of each device from one well to another
    drilling_time = np.zeros(M)  # a vector containing the drilling time for each devices

    # selects the M wells that are closest to the depot
    index = np.argsort(devices_travel_time[0, :])  # sorts the wells from the closest to the farthest in terms of travel time
    for i in range(1,M+1): 
        displacements[i-1].append(int(index[i]))  # assigns the M devices to the m wells closest to the depot
        Wells.remove(index[i])  # removes wells that have already been drilled from the list or set
        drilling_time[i-1] += devices_travel_time[0, int(index[i])] + int(well_drilling_time[int(index[i])-1])
        for j in range(N+1):  # sets the travel time to infinity between the newly added well in the sequence and all other wells
            devices_travel_time[j][int(index[i])] = 1000

    # set the travel time between each well and itself to infinity
    for j in range(N+1):
        devices_travel_time[j][j] = 1000  # time travel between well and itself
        devices_travel_time[j][0] = 1000  # time travel between eah well and depot

    while len(Wells) >= M:             
        for k in range(M):
            j = len(displacements[k])  # selects the last well drilled by device k
            #x = devices_travel_time[int(displacements[k][j-1])].index(min(devices_travel_time[int(displacements[k][j-1])])) # selects the well that is closest in travel time
            x = np.argmin(devices_travel_time[int(displacements[k][j-1])])
            displacements[k].append(int(x))  # adds the selected well to the current drilling sequence 
            Wells.remove(int(x))  # removes the selected well from the set of available wells
            drilling_time[k] += min(devices_travel_time[int(displacements[k][j-1])]) + int(well_drilling_time[int(x)-1])
            for i in range(N+1):
                devices_travel_time[i][x] = 1000  

    while len(Wells) >= 1:
        k = random.randrange(0, M) 
        j = len(displacements[k])  # selects the last well drilled by device k
        #x = devices_travel_time[int(displacements[k][j-1])].index(min(devices_travel_time[int(displacements[k][j-1])]))  # selects the well that is closest in travel time
        x = np.argmin(devices_travel_time[int(displacements[k][j-1])])
        displacements[k].append(int(x))  # adds the selected well to the current drilling sequence 
        Wells.remove(int(x))  # removes the selected well from the set of available wells
        drilling_time[k] += min(devices_travel_time[int(displacements[k][j-1])]) + int(well_drilling_time[int(x)-1])
        for i in range(N+1):  
                devices_travel_time[i][x] = 1000
    
    Total_time = np.max(drilling_time)   # total time of drilling     
    
    return displacements, Total_time



def insertion(travel_time, drilling, M):

    devices_travel_time = travel_time.to_numpy()  # convert the DataFrame to a NumPy array for further processing
    devices_travel_time = devices_travel_time[:,1:]  # remove the column containing the well names
    well_drilling_time = drilling.to_numpy()  
    well_drilling_time = well_drilling_time[:,1]  


    T = np.copy(devices_travel_time)

    N = len(devices_travel_time) - 1 # number of wells


    # constructs the set of all wells and devices
    Wells = []  # wells set
    Devices = []  # devices set

    for i in range(1,N+1): 
        Wells.append(i)   
    for k in range(1, M+1):
        Devices.append(k)

    displacements = [[0] for _ in range(M)]  # a vector containing the movement of each device from one well to another
    drilling_time = np.zeros(M)  # a vector containing the drilling time for each devices

    # selects the M wells that are closest to the depot
    index = np.argsort(devices_travel_time[0, :])  # sorts the wells from the closest to the farthest in terms of travel time
    for k in range(1,M+1): 
        displacements[k-1].append(int(index[k]))  # assigns the M devices to the m wells closest to the depot
        Wells.remove(index[k])  # removes wells that have already been drilled from the list or set
        for i in range(N+1):  # sets the travel time to infinity between the newly added well in the sequence and all other wells
            devices_travel_time[i][int(index[k])] = 1000

    # set the travel time between each well and itself to infinity
    for i in range(N+1):
        devices_travel_time[i][i] = 1000  # time travel between well and itself
        devices_travel_time[i][0] = 1000  # time travel between eah well and depot

    
    while len(Wells) >= M:
        for k in range(M):
            D=[]
            for j in displacements[k]:
                if (j != 0):
                   D.append(j)
            P = Wells 

            Matrix = devices_travel_time[np.ix_(D, P)]
            min_index = np.unravel_index(np.argmin(Matrix), Matrix.shape)
            z1 = displacements[k][int(min_index[0])+1]
            z2 = P[min_index[1]]

            if (min_index[0] == 0):
               displacements[k].insert(min_index[0]+2 , z2)
            else:
                S1 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]-1]] + devices_travel_time[displacements[k][min_index[0]-1]][displacements[k][min_index[0]]]
                S2 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]+1]] + devices_travel_time[displacements[k][min_index[0]+1]][displacements[k][min_index[0]]]
                if (S1 < S2):
                    displacements[k].insert(min_index[0]+1, z2)
                else:
                    displacements[k].insert(min_index[0]+2, z2)

            Wells.remove(z2)

            for i in range(N+1):
                devices_travel_time[i][z2] = 1000
        
    
    while (len(Wells) >= 1):
        k = random.randrange(0, M) 
        D=[]

        for j in displacements[k]:
            if (j != 0):
               D.append(j)
        P = Wells 

        Matrix = devices_travel_time[np.ix_(D, P)]
        min_index = np.unravel_index(np.argmin(Matrix), Matrix.shape)
        z1 = displacements[k][int(min_index[0])+1]
        z2 = P[min_index[1]]

        if (min_index[0] == 0):
           displacements[k].insert(min_index[0]+2 , z2)
        else:
            S1 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]-1]] + devices_travel_time[displacements[k][min_index[0]-1]][displacements[k][min_index[0]]]
            S2 = devices_travel_time[displacements[k][min_index[0]]][z2] + devices_travel_time[z2][displacements[k][min_index[0]+1]] + devices_travel_time[displacements[k][min_index[0]+1]][displacements[k][min_index[0]]]
            if (S1 < S2):
                displacements[k].insert(min_index[0]+1, z2)
            else:
                displacements[k].insert(min_index[0]+2, z2)

        Wells.remove(z2)

        for i in range(N+1):
            devices_travel_time[i][z2] = 1000
        
    for k in range(M):
        for j in range(len(displacements[k])-1):
            drilling_time[k] += T[displacements[k][j]][displacements[k][j+1]] + well_drilling_time[displacements[k][j+1]-1]

    
    Total_time = np.max(drilling_time)

    return displacements, Total_time
    
