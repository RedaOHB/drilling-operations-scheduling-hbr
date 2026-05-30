import numpy as np
import copy
import random

def Time(displacements, devices_travel_time, well_drilling_time):
    
    m = len(displacements)  # number of devices

    drillig_time = np.zeros(m)

    for k in range(m):
        for j in range(len(displacements[k])-1):
            drillig_time[k] += devices_travel_time[displacements[k][j]][displacements[k][j+1]] + well_drilling_time[displacements[k][j+1]-1]


    return drillig_time


def neighborhood(displacements, devices_travel_time, well_drilling_time, N):

    disp = copy.deepcopy(displacements)

    drilling_time = Time(displacements, devices_travel_time, well_drilling_time)
    
    if N == 1:

        y_min = np.argmin(drilling_time)    
        y_max = np.argmax(drilling_time)

        z = random.randint(2, len(disp[y_max])-1)
        k = disp[y_max].pop(z)

        disp[y_min].insert(2, k)
        f = np.max(Time(disp, devices_travel_time, well_drilling_time))

        displacements_1 = copy.deepcopy(disp)
        T = len(disp[y_min])


        for j in range(3, T):
            disp_1 = copy.deepcopy(disp)
            disp_1[y_min].remove(k)
            disp_1[y_min].insert(j, k)
            f_1 = np.max(Time(disp_1, devices_travel_time, well_drilling_time))

            if (f_1 < f):
                displacements_1 = disp_1
                f = f_1

        return displacements_1

    else:
        if N == 2:

            index = np.argsort(drilling_time)

            z1 = int(index[len(index)-1])
            z2 = int(index[len(index)-2])

            for z in [z1, z2]:
                l = random.randint(2,len(disp[z])-4)
                i = l 
                j = l+3

                while (i <= l+3/2) & (j >= l+3/2):
                    k = disp[z][i]
                    disp[z][i] = disp[z][j]
                    disp[z][j] = k
                    i += 1
                    j -= 1

            return disp
        
        else: 

            y_max = np.argmax(drilling_time)
            values = [i for i in range(0, len(disp)) if i != y_max]
            y = random.choice(values)

            z1=random.randint(2,len(disp[y_max])-3)
            z2=random.randint(2,len(disp[y])-3)

            for j in range(3):
                k = disp[y_max][z1+j]
                disp[y_max][z1+j] = disp[y][z2+j]
                disp[y][z2+j] = k



        return disp
    

def local_search(displacements, devices_travel_time, well_drilling_time):
    disp = copy.deepcopy(displacements)
    F = np.max(Time(displacements, devices_travel_time, well_drilling_time))

    i = 1
    k_max = 3  # three neighborhoods

    while i <= k_max:
        displacements_1 = neighborhood(disp,devices_travel_time, well_drilling_time, i)
        F_1 = np.max(Time(displacements_1, devices_travel_time, well_drilling_time))

        if (F_1 < F):
            disp = copy.deepcopy(displacements_1)
            F = F_1
            i = 1
        else:
            i = i + 1
    
    return disp


 