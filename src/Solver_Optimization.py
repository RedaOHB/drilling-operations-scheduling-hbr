import numpy as np
import pandas as pd
from gurobipy import Model, GRB, quicksum




def solve_PL(P, R, h, T):

    m = Model()

    
    # --------------- Variables
    Y = m.addVars(P, P, R, vtype=GRB.BINARY, name="Y")
    W = m.addVar(vtype=GRB.CONTINUOUS, lb=0, name="W")

    # --------------- Objective
    m.setObjective(W, GRB.MINIMIZE)

    # --------------- Constraints
    # 1)
    for k in R:
        m.addConstr(
            quicksum((h[i] + T[i, j]) * Y[i, j, k]
                     for i in P for j in P) <= W
        )

    # 2)
    for k in R:
        m.addConstr(quicksum(Y[0, j, k] for j in P if j != 0) == 1)

    # 3)
    for i in P:
        if i != 0:
            m.addConstr(quicksum(Y[i, j, k] for j in P for k in R) == 1)

    # 4)
    for j in P:
        if j != 0:
            m.addConstr(quicksum(Y[i, j, k] for i in P for k in R) == 1)

    # 5)
    for k in R:
        m.addConstr(quicksum(Y[i, 0, k] for i in P if i != 0) == 1)

    # 6)
    for i in P:
        for k in R:
            m.addConstr(Y[i, i, k] == 0)

    # 7)
    for i in P:
        for j in P:
            if i != j:
                m.addConstr(
                    quicksum(Y[i, j, k] + Y[j, i, k] for k in R) <= 1
                )

    # 8)
    for l in P:
        for k in R:
            m.addConstr(
                quicksum(Y[i, l, k] for i in P) ==
                quicksum(Y[l, j, k] for j in P)
            )

    # --------------- Solve
    m.optimize()

    # --------------- Result
    if m.status == GRB.OPTIMAL:
        return {
            "W": W.X,
            "Y": {(i, j, k): Y[i, j, k].X
                  for i in P for j in P for k in R}
        }
    else:
        return None
    

# ----------------------- main script -------------------------------------

travel_time = pd.read_excel("data\Data.xlsx", sheet_name=1)
drilling = pd.read_excel("data\Data.xlsx", sheet_name=2)

N = 25
M = 2
                                                            
devices_travel_time = travel_time.to_numpy()  # convert the DataFrame to a NumPy array for further processing
devices_travel_time = devices_travel_time[:,1:]  # remove the column containing the well names
well_drilling_time = drilling.to_numpy() 
well_drilling_time = well_drilling_time[:,1]

P = range(N)
R = range(M)

solution = solve_PL(P, R, well_drilling_time, devices_travel_time)


print(solution["W"])  
