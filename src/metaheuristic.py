import numpy as np
import copy
from utils import neighborhood, Time, local_search


def variable_neighborhood_search(displacements, devices_travel_time, well_drilling_time):
    
    F = np.max(Time(displacements, devices_travel_time, well_drilling_time))
    k_max = 3
    iteration = 1

    while iteration <= 5000:
        k = 1

        while (k <= k_max):
           displacements_1 = neighborhood(copy.deepcopy(displacements), devices_travel_time, well_drilling_time, k)
           displacements_2 = local_search(copy.deepcopy(displacements_1), devices_travel_time, well_drilling_time)

           F_2 = np.max(Time(displacements_2, devices_travel_time, well_drilling_time))

           if (F_2 < F):
               displacements = copy.deepcopy(displacements_2)
               F = F_2
               k = 1
           else:
               k = k + 1
                 
        iteration = iteration + 1
        print(iteration)

    total_time = np.max(Time(displacements, devices_travel_time, well_drilling_time))



    return displacements, total_time
          
     

     





