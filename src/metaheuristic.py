import numpy as np
import copy
from utils import neighborhood, Time, local_search


"""
  variable_neighborhood_search(displacements, devices_travel_time, well_drilling_time)

  implements Variable Neighborhood Search (VNS) metaheuristic via three neighborhoods and local research 

  # Parameters: 

   - `displacements`: routing sequence for each device (Vector)
   - `devices_travel_time`: travel time between wells for each device (Matrix)
   - `well_drilling_time`: drilling time required for each well (Vector)

  # Result: 
   
   - `displacements`: routing sequence for each device
   - `Total_time`: total time required to complete the drilling of all wells
"""

def variable_neighborhood_search(displacements, devices_travel_time, well_drilling_time):
    
    F = np.max(Time(displacements, devices_travel_time, well_drilling_time))  # total drilling time of the current solution
    k_max = 3  # number of neighborhoods
    iteration = 1

    while iteration <= 5000:  # maximum number of iterations (stopping criterion).
        k = 1  

        while (k <= k_max):
           displacements_1 = neighborhood(copy.deepcopy(displacements), devices_travel_time, well_drilling_time, k)  # apply the k-th neighborhood
           displacements_2 = local_search(copy.deepcopy(displacements_1), devices_travel_time, well_drilling_time)  # apply local search

           F_2 = np.max(Time(displacements_2, devices_travel_time, well_drilling_time))  # total drilling time of the new solution

           if (F_2 < F):  # if the new solution is better 
               displacements = copy.deepcopy(displacements_2)
               F = F_2  # keep the new solution
               k = 1
           else:  # otherwise, move to the next neighborhood
               k = k + 1
                 
        iteration = iteration + 1

    total_time = np.max(Time(displacements, devices_travel_time, well_drilling_time))  # total drilling time   



    return displacements, total_time
          
     

     





