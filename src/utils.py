import numpy as np
import copy
import random

"""
  Time(displacements, devices_travel_time, well_drilling_time)

  calculates the total drilling time for each root

  # Parameters: 

   - `displacements`: routing sequence for each device (Vector)
   - `devices_travel_time`: travel time between wells for each device (Matrix)
   - `well_drilling_time`: drilling time required for each well (Vector)

  # Result: 
   
   - `drilling_time`: total time required to complete the drilling of all wells
"""

def Time(displacements, devices_travel_time, well_drilling_time):
     
    m = len(displacements)  # number of devices  

    drillig_time = np.zeros(m)

    for k in range(m):  
        for j in range(len(displacements[k])-1):
            drillig_time[k] += devices_travel_time[displacements[k][j]][displacements[k][j+1]] + well_drilling_time[displacements[k][j+1]-1]
        drillig_time[k] += devices_travel_time[displacements[k][len(displacements[k])-1]][0]             


    return drillig_time


"""
  neighborhood(displacements, devices_travel_time, well_drilling_time, N)

  searches for a neighboring solution of the current solution within a specified neighborhood

  # Parameters: 

   - `displacements`: routing sequence for each device (Vector)
   - `devices_travel_time`: travel time between wells for each device (Matrix)
   - `well_drilling_time`: drilling time required for each well (Vector)
   - `N`: index of neighborhood

  # Result: 
   
   - `displacements` or `disp`: routing sequence for each device 
"""

def neighborhood(displacements, devices_travel_time, well_drilling_time, N):

    disp = copy.deepcopy(displacements)  

    drilling_time = Time(displacements, devices_travel_time, well_drilling_time)  # drilling time of the current solution
    
    if N == 1:  # the first neighborhood

        y_min = np.argmin(drilling_time)  # index of the route with the smallest drilling time
        y_max = np.argmax(drilling_time)  # index of the route with the largest drilling time

        z = random.randint(2, len(disp[y_max])-1)  # select a random position
        k = disp[y_max].pop(z)  # remove the element at position z from the route with the largest drilling time

        disp[y_min].insert(2, k)  # insert k into the route with the smallest drilling time
        f = np.max(Time(disp, devices_travel_time, well_drilling_time))  # total drilling time of the new route

        displacements_1 = copy.deepcopy(disp) 
        T = len(disp[y_min])


        for j in range(3, T):  # try multiple positions for k
            disp_1 = copy.deepcopy(disp)
            disp_1[y_min].remove(k)  # remove k 
            disp_1[y_min].insert(j, k)  # insert k at another position
            f_1 = np.max(Time(disp_1, devices_travel_time, well_drilling_time))  # calulate the total drilling time

            if (f_1 < f):  # if the new solution is better than previous one
                displacements_1 = disp_1  # keep the new solution
                f = f_1

        return displacements_1

    else:
        if N == 2:  # the second neighborhood

            index = np.argsort(drilling_time)  # sort the drilling time

            z1 = int(index[len(index)-1])  # index of the route with the smallest drilling time
            z2 = int(index[len(index)-2])  # index of the root before 

            for z in [z1, z2]:  # for each selected root
                l = random.randint(2,len(disp[z])-4)  # select a random position
                i = l 
                j = l+3 

                while (i <= l+3/2) & (j >= l+3/2):  # reverse the sequence between positions i and j
                    k = disp[z][i]
                    disp[z][i] = disp[z][j]
                    disp[z][j] = k
                    i += 1
                    j -= 1

            return disp
        
        else:  # the third neighborhood

            y_max = np.argmax(drilling_time)  # index of the root with largest drilling time
            values = [i for i in range(0, len(disp)) if i != y_max]  
            y = random.choice(values)  # select a route randomly

            # select a random position in each selected route
            z1=random.randint(2,len(disp[y_max])-3)
            z2=random.randint(2,len(disp[y])-3)

            for j in range(3):  # reverse the selected sequences between the two selected routes
                k = disp[y_max][z1+j]
                disp[y_max][z1+j] = disp[y][z2+j]
                disp[y][z2+j] = k



        return disp


"""
  local_search(displacements, devices_travel_time, well_drilling_time)

  search a neighbor solution of the current solution via a set of neighborhood

  # Parameters: 

   - `displacements`: devices routing (Vector)
   - `devices_travel_time`: devices travel time between wells (Matrix)
   - `well_drilling_time`: drilling time of each well (Vector)

  # Result: 
   
   - `dis`: devices routing
"""

def local_search(displacements, devices_travel_time, well_drilling_time):

    disp = copy.deepcopy(displacements)  
    F = np.max(Time(displacements, devices_travel_time, well_drilling_time))  # drilling time of the current solution
    

    i = 1  # neighborhood index
    k_max = 3  # three neighborhoods

    while i <= k_max:  
        displacements_1 = neighborhood(disp,devices_travel_time, well_drilling_time, i)  # generate a new solution using neighborhood "i"
        F_1 = np.max(Time(displacements_1, devices_travel_time, well_drilling_time))  # total drilling time of the new solution

        if (F_1 < F):  # if the new solution is better than the previous one
            disp = copy.deepcopy(displacements_1)
            F = F_1  # keep the new solution
            i = 1
        else:  # change the neighborhood
            i = i + 1
    
    return disp


 