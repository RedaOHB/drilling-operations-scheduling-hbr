import numpy as np
import pandas as pd
import random
import copy 
from heuristics import nearest_neighbor, insertion
from utils import neighborhood, local_search, Time
from metaheuristic import variable_neighborhood_search


travel_time = pd.read_excel("data\Data.xlsx", sheet_name=1)
drilling = pd.read_excel("data\Data.xlsx", sheet_name=2)
M = 2

devices_travel_time = travel_time.to_numpy()  # convert the DataFrame to a NumPy array for further processing
devices_travel_time = devices_travel_time[:,1:]  # remove the column containing the well names
well_drilling_time = drilling.to_numpy()  
well_drilling_time = well_drilling_time[:,1]


displacements, total_time = insertion(travel_time, drilling, M)

print(displacements)
print(total_time)

X = variable_neighborhood_search(displacements, devices_travel_time, well_drilling_time) 


print(X[0])
print(X[1])



