# -*- coding: utf-8 -*-
# @Author: Lei Liu
# @Date:   2020-08-25 16:45:49
# @Last Modified by:   Lei Liu
# @Last Modified time: 2020-09-14 22:46:09



#  have a known schedule, calculate its obj, such as total completion time.
#  with disjunctive constraints/ or half disjunctive constraints


'''
Now this code can deal with without re-entrant and with re-entrant, half re-entrant 

All scenarios

'''

from gurobipy import *


num_job = 6
num_machine= 5 

# process_scenario= [
#              [63, 23, 69, 36, 30, 10],
#              [34, 9, 46, 13, 19, 26],
#              [5, 21, 29, 40, 10, 70],
#              [0, 0,  0, 0, 0,  0],
#              [0, 0,  0, 0, 0,  0]
#              ]

# process_scenario= [
#             [74, 89, 416, 63, 59, 76],
#             [103, 23, 89, 66, 90, 50],
#             [65, 221, 89, 60, 100, 130],
#             [103, 23, 89, 66, 90, 50],
#             [65, 221, 89, 60, 100, 130]
#             ]


# process_scenario= [
#                     [70,  53,  302,50,  30, 76],
#                     [100, 20, 50,   13,  29, 40],
#                     [40,  121, 89, 40,  90, 80],
#                     [0, 0,  0, 0, 0,  0],
#                     [0, 0,  0, 0, 0,  0]
            # ]
# process_scenario= [[70,  53,  302,50,  30, 76],
#                     [100, 20, 50,   13,  29, 40],
#                     [40,  121, 89, 40,  90, 80],
#                     [100, 20, 50,   13,  29, 40],
#                     [40,  121, 89, 40,  90, 80]]

# process_scenario= [[63, 23, 69, 36, 30, 10],
#              [34, 9, 46, 13, 19, 26],
#              [5, 21, 29, 40, 10, 70],
#                  [34, 0,  46, 0, 0,  26],
#              [0, 21,  0, 0, 0,  70]]

# process_scenario = [[74, 89, 416, 63, 59, 76],
#                     [103, 23, 89, 66, 90, 50],
#                     [65, 221, 89, 60, 100, 130],
#                     [103, 0, 89, 66, 90, 0],
#                     [65, 221, 0, 60, 0, 130]]

# process_scenario = [[70,  53,  302,50,  30, 76],
#                     [100, 20, 50,   13,  29, 40],
#                     [40,  121, 89, 40,  90, 80],
#                     [0, 20, 50,   13,  0, 40],
#                     [40,  121, 0, 40,  90, 0]]

process_scenario =  [[74, 23, 69, 63, 30, 76], 
                    [103, 9, 46, 66, 19, 50], 
                    [65, 21, 29, 60, 10, 130], 
                    [0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0]]

schedule = [5,0,3,4,2,1]

# [5,0,3,4,2,1]
# [4,1,5,0,3,2]
# [3,5,0,4,2,1]
# [3,4,5,1,0,2]
# [3,4,0,5,2,1]
# [1,3,4,5,2,0]
# [3,4,5,0,1,2]
# [4,3,1,5,0,2]




# index_i         = range(num_job)
pos_j           = range(num_job)
index_m         = range(num_machine)


def calTotal_C():

    model = Model("flow_shop_schedule")
    TotalC = model.addVar(lb = 0,  name = "TotalC")
    Start = model.addVars(pos_j, index_m,  name="S")
    ComP = model.addVars(pos_j, index_m,  name="C")
    
    delta4  = model.addVars(pos_j, pos_j, vtype=GRB.BINARY, name = "delta4")
    delta3  = model.addVars(pos_j, pos_j, vtype=GRB.BINARY, name = "delta3")

    model.setObjective(TotalC, GRB.MINIMIZE)
    model.addConstr(TotalC == quicksum(ComP[(j,num_machine-1)] for j in pos_j))
    model.addConstrs(((ComP[(j,k)] == Start[(j,k)] +  process_scenario[k][schedule[j]] ) for j in pos_j for k in index_m), name = "Cjk")
    model.addConstrs((Start[(j,k)] >= ComP[(j,k-1)] for j in pos_j for k in range(1, num_machine)), name = "Sjk1")
    model.addConstrs((Start[(j,k)] >= ComP[(j-1,k)] for j in range(1, num_job) for k in index_m), name = "Sjk2")
        
    model.addConstrs((Start[(j,2)] >= ComP[(jprime, 4)] - delta3[(j, jprime)]*10000 
                        for j in pos_j for jprime in pos_j if j > jprime if process_scenario[4][j]>0 if process_scenario[4][jprime]>0), name = "disjunctive1")
    
    model.addConstrs((Start[(jprime,4)] >= ComP[(j, 2)] - (1-delta3[(j, jprime)])*10000 
                        for j in pos_j for jprime in pos_j if j > jprime if process_scenario[4][j]>0 if process_scenario[4][jprime]>0), name = "disjunctive2")
    

    model.addConstrs((Start[(j,1)] >= ComP[(jprime, 3)] - delta4[(j, jprime)]*10000 
                        for j in pos_j for jprime in pos_j if j > jprime if process_scenario[3][j]>0 if process_scenario[3][jprime]>0), name = "disjunctive3")
    
    model.addConstrs((Start[(jprime,3)] >= ComP[(j, 1)] - (1-delta4[(j, jprime)])*10000 
                        for j in pos_j for jprime in pos_j  if j > jprime if process_scenario[3][j]>0 if process_scenario[3][jprime]>0), name = "disjunctive4")
    
    # model.Params.LogToConsole=False
    model.optimize()
    obj = model.getObjective()
    print(obj.getValue())
    # vars =  model.getVars()
    # for i in range(61):
    #     print('%s %g' % (vars[i].varName, vars[i].x))


if __name__ == '__main__':
    calTotal_C()
