# -*- coding: utf-8 -*-
# @Author: Lei Liu
# @Date:   2020-08-24 17:27:34
# @Last Modified by:   Lei Liu
# @Last Modified time: 2020-09-19 16:16:27



#  given a new scenario, calculate the optimal schedule and total completion time
#  pay attention to the disjunctive constraints, 


from gurobipy import *

num_job = 6
num_machine= 5 

process_scenario =  [[74, 23, 69, 63, 30, 76], 
                    [103, 9, 46, 66, 19, 50], 
                    [65, 21, 29, 60, 10, 130], 
                    [0, 0, 0, 0, 0, 0], 
                    [0, 0, 0, 0, 0, 0]]

     
index_i         = range(num_job)
pos_j           = range(num_job)
index_m         = range(num_machine)

def TotalC_Opt(disjunctive):
    modelstar = Model("optimal_problem")
    y     = modelstar.addVars(index_i, pos_j,  vtype=GRB.BINARY, name="y")
    TotalC = modelstar.addVar(lb = 0,  name = "TotalC")
    Sstar = modelstar.addVars(pos_j, index_m,   name="Sstar")
    Cstar = modelstar.addVars(pos_j, index_m,   name="Cstar")
    delta4  = modelstar.addVars(pos_j, pos_j, vtype=GRB.BINARY, name = "delta4")
    delta3  = modelstar.addVars(pos_j, pos_j, vtype=GRB.BINARY, name = "delta3")
    
    



    modelstar.setObjective(TotalC, GRB.MINIMIZE)
    modelstar.addConstr(TotalC == quicksum(Cstar[(j,num_machine-1)] for j in pos_j))

    modelstar.addConstrs((Cstar[(j,k)] == Sstar[(j,k)] + quicksum(y[(i,j)] * process_scenario[k][i]  for i in index_i) for j in pos_j for k in index_m), name = "Cjk")
    
    modelstar.addConstrs((Sstar[(j,k)] >= Cstar[(j,k-1)] for j in pos_j for k in range(1, num_machine)), name = "Sjk1")
    modelstar.addConstrs((Sstar[(j,k)] >= Cstar[(j-1,k)] for j in range(1, num_job) for k in index_m), name = "Sjk2")
    
    
    modelstar.addConstrs((Sstar[(j,2)] >= Cstar[(jprime, 4)] - delta3[(j, jprime)]*10000 
            for j in pos_j for jprime in pos_j if j > jprime if process_scenario[4][j]>0 if process_scenario[4][jprime]>0), name = "disjunctive1")
    modelstar.addConstrs((Sstar[(jprime,4)] >= Cstar[(j, 2)] - (1-delta3[(j, jprime)])*10000 
            for j in pos_j for jprime in pos_j if j > jprime if process_scenario[4][j]>0 if process_scenario[4][jprime]>0), name = "disjunctive2")

    modelstar.addConstrs((Sstar[(j,1)] >= Cstar[(jprime, 3)] - delta4[(j, jprime)]*10000 
            for j in pos_j for jprime in pos_j if j > jprime if process_scenario[3][j]>0 if process_scenario[3][jprime]>0), name = "disjunctive3")
    modelstar.addConstrs((Sstar[(jprime,3)] >= Cstar[(j, 1)] - (1-delta4[(j, jprime)])*10000 
                    for j in pos_j for jprime in pos_j  if j > jprime if process_scenario[3][j]>0 if process_scenario[3][jprime]>0), name = "disjunctive4")
    
    for i in range(num_job):
        modelstar.addConstr(sum(y[(i,j)] for j in range(num_job)) == 1)
    for j in range(num_job):
        modelstar.addConstr(sum(y[(i,j)] for i in range(num_job)) == 1)
    
    modelstar.Params.LogToConsole=False
    modelstar.optimize()

    print('-------------The Optimizaiton Problem Results-------------------------')
    vars =  modelstar.getVars()
    for i in range(36):
         # print('%s %g' % (vars[i].varName, vars[i].x))
        if(vars[i].x == 1):
           print('%s %g' % (vars[i].varName, vars[i].x))
    
    print('-------------TotalC------------------------')
    for i in range(36, 37):
         print('%s %g' % (vars[i].varName, vars[i].x))    
    
    
    
    return modelstar.objVal




if __name__ == '__main__':
    TotalC_Opt(1)