import numpy as np
import pandas as pd
import random
import copy 
from heuristics import nearest_neighbor, insertion  # import heuristics functions
from utils import neighborhood, local_search, Time  # import and helper functions
from metaheuristic import variable_neighborhood_search  # import metaheuristic function


travel_time = pd.read_excel("data\Data.xlsx", sheet_name=1)  # import data: travel time inter-well
drilling = pd.read_excel("data\Data.xlsx", sheet_name=2)  # import data: drilling time of each well
M = 2  # number of devices

# convert the DataFrame to a NumPy array for further processing
devices_travel_time = travel_time.to_numpy()  
well_drilling_time = drilling.to_numpy()  
# remove the column containing the well names
devices_travel_time = devices_travel_time[:,1:]  
well_drilling_time = well_drilling_time[:,1]

# generate an initial solution using a heuristic (Nearest Neighbor or Insertion)
displacements, total_time = nearest_neighbor(travel_time, drilling, M)
displacements, total_time = insertion(travel_time, drilling, M)

print("Solution founded by heuristic:")
for k, route in enumerate(displacements):
    print(f"  Rig {k+1}: {route}")

print(f"Total time of drilling is : {total_time} days")

# apply a metaheuristic to improve the current solution
X = variable_neighborhood_search(displacements, devices_travel_time, well_drilling_time) 

print("Solution founded by heuristic:")
for k, route in enumerate(X[0]):
    print(f"  Rig {k+1}: {route}")

print(f"Total time of drilling is : {X[1]} days")



