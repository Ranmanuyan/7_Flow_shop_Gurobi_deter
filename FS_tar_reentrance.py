#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 15:30:40 2020

@author: liulei
"""



"""
1, A modified model of minimizing the makespan of flow shop scheduling (using start time).

2, Add the re-entrance constraints 

3, modify as total tardiness minimization ----------            3 July 2020

"""
 
from gurobipy import *

try:
	# define parameters
    m               = 7
    n               = 5          
    index_i         = range(n)
    pos_j           = range(n)
    index_m         = range(m)
    pt              = [[ 34,  59,  6,  46, 6, 46, 38],
                       [63, 3, 69, 38,69, 38,  36],
                       [5, 11, 29, 21,29, 21, 20],
                       [51, 9  , 15  ,48  ,15  ,48  ,65],
                       [57, 36  , 69  ,68  ,69  ,68  ,33]]
#                       [36, 70, 45, 91, 35],
#                       [53  ,99  , 60 , 13 ,53],
#                       [38 , 60  , 23  , 59  , 41],
#                       [27  ,  5  , 57  , 49  , 69],
#                       [87  , 56  , 64  , 85  , 13],
#                       [76  , 3  ,  7  , 85  , 86],
#                       [91  , 61  ,  1  ,  9  , 72],
#                       [14  , 73  , 63  , 39 ,  8],
#                       [29  , 75  , 41  , 41  , 49],
#                       [12  , 47  , 63  , 56  , 47],
#                       [77  , 14  , 47  , 40  , 87],
#                       [32 , 21  , 26  , 54 , 58],
#                       [87  , 86  , 75 , 77  , 18],
#                       [68  , 5  , 77  , 51  , 68],
#                       [94  , 77  , 40 , 31  , 28]]    
    
    
due             =  [367, 370,328, 1239, 191 ] # , 592, 771, 503, 539, 805, 1025, 602, 525, 482, 823, 568, 533, 743,495, 607]


	# Create a new model
    model = Model("flow_shop_schedule_tardiness")
	
	# Create variables
    # delta1  = model.addVars(pos_j, pos_j,  vtype=GRB.BINARY, name = "delta1")    
    x     = model.addVars(index_i, pos_j, vtype=GRB.BINARY, name="x")
    S     = model.addVars(pos_j, index_m,  vtype=GRB.INTEGER,name="S")
    C     = model.addVars(pos_j, index_m,  vtype=GRB.INTEGER,name="C")
    # Cmax = model.addVar(vtype=GRB.INTEGER,name="Cmax")
    delta1  = model.addVars(pos_j, pos_j,  vtype=GRB.BINARY, name = "delta1")
    delta2  = model.addVars(pos_j, pos_j, vtype=GRB.BINARY, name = "delta2")
    T     = model.addVars(pos_j, vtype=GRB.INTEGER, name = "T")
    w     = model.addVars(pos_j, lb = -100000, vtype=GRB.INTEGER, name = "w")


    
    
    # Set objective
    # Set objective
    model.setObjective(quicksum(T[j]  for j in pos_j ), GRB.MINIMIZE)
    
    # Add constraints 

    model.addConstrs((w[j] == C[(j,m-1)] - (quicksum(x[(i,j)]*due[i] 
                                for i in index_i)) for j in pos_j), name = "cons1")
    
    model.addConstrs( (T[j] == max_(w[j], 0) for j in pos_j), name = "cons2")
    
	
	# Add constraints 
    # model.addConstrs((Cmax >= C[(j,m-1)] for j in pos_j), name ="CmaxCons")
    model.addConstrs((C[(j,k)] == S[(j,k)] + quicksum(x[(i,j)] * pt[i][k]  for i in index_i) for j in pos_j for k in index_m), name = "Cjk")
    
    model.addConstrs((S[(j,k)] >= C[(j,k-1)] for j in pos_j for k in range(1, m)), name = "Sjk1")
    model.addConstrs((S[(j,k)] >= C[(j-1,k)] for j in range(1, n) for k in index_m), name = "Sjk2")
        
#    model.addConstrs(( C[(0, k)] >= quicksum(x[(i,0)] * pt[i][a]  for i in index_i for a in range(k+1) )for k in index_m), name = "cons3"
#    model.addConstrs(( C[(j, 0)] >= quicksum(x[(i,j)] * pt[i][0]  for i in index_i) + C[(j-1,0)]  for j in range(1,n)), name = "cons4")
    model.addConstrs((S[(j,2)] >= C[(jprime, 4)] - delta1[(j, jprime)]*10000 
                        for j in pos_j for jprime in pos_j if j > jprime), name = "disjunctive1")
    
    model.addConstrs((S[(jprime,4)] >= C[(j, 2)] - (1-delta1[(j, jprime)])*10000 
                        for j in pos_j for jprime in pos_j if j > jprime), name = "disjunctive2")
    

    model.addConstrs((S[(j,3)] >= C[(jprime, 5)] - delta1[(j, jprime)]*10000 
                        for j in pos_j for jprime in pos_j if j > jprime), name = "disjunctive3")
    
    model.addConstrs((S[(jprime,5)] >= C[(j, 3)] - (1-delta1[(j, jprime)])*10000 
                        for j in pos_j for jprime in pos_j if j > jprime), name = "disjunctive4")

    

    for i in range(n):
        model.addConstr(sum(x[(i,j)] for j in range(n)) == 1)
    for j in range(n):
        model.addConstr(sum(x[(i,j)] for i in range(n)) == 1)
    
	# optimize!
    model.optimize()
	
	# print out the objective function value
    print('Obj: %g' % model.objVal)
    vars =  model.getVars()
    for i in range(25):
        if(vars[i].x == 1):
         print('%s %g' % (vars[i].varName, vars[i].x))
#    for i in range(25, 95):
#         print('%s %g' % (vars[i].varName, vars[i].x))
#    
    
    
    
    
    
    
# : exceptions :
except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')