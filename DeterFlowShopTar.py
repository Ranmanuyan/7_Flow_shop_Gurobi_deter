#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 10:23:38 2020

@author: liulei
"""

from gurobipy import *

try:
	# define parameters
    m               = 5
    n               = 5          
    index_i         = range(n)
    pos_j           = range(n)
    index_m         = range(m)
    pt              = [[ 54,  79,  16,  66, 58],
                       [83, 3, 89, 58,  56],
                       [15, 11, 49, 31, 20],
                       [71, 99  , 15  ,68  ,85],
                       [77, 56  , 89  ,78  ,53]]
                       
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
    model = Model("flow_shop_schedule")
	
	# Create variables
    
    x     = model.addVars(index_i, pos_j, vtype=GRB.BINARY, name="x")
    C     = model.addVars(pos_j, index_m,  vtype=GRB.INTEGER,name="C")


    T     = model.addVars(pos_j, vtype=GRB.INTEGER, name = "T")

    #
    w     = model.addVars(pos_j, lb = -100000, vtype=GRB.INTEGER, name = "w")
    y     = model.addVars(pos_j, index_m, vtype=GRB.INTEGER, name = "y")


	# Set objective
    model.setObjective(quicksum(T[j]  for j in pos_j ), GRB.MINIMIZE)
	
	# Add constraints 

    model.addConstrs((w[j] == C[(j,m-1)] - (quicksum(x[(i,j)]*due[i] 
                                for i in index_i)) for j in pos_j), name = "cons1")
    
    model.addConstrs( (T[j] == max_(w[j], 0) for j in pos_j), name = "cons2")
    
    model.addConstrs((C[(0, k)] ==  quicksum(x[(i,0)] * pt[i][a] for i in index_i for a in range(k+1) )for k in index_m), name = "cons3")
    
    model.addConstrs((C[(j, 0)] ==  quicksum(x[(i,j)] * pt[i][0] for i in index_i) + C[(j-1,0)]  for j in range(1,n)), name = "cons4")

    model.addConstrs( y[(j,0)] == 0 for j in pos_j )
    model.addConstrs( y[(0,k)] == 0 for k in index_m )
    
    model.addConstrs((y[(j,k)] == max_(C[(j-1,k)], C[(j,k-1)]) for j in range(1,n) for k in range(1, m) ) ,name = "cons5")

    model.addConstrs( (C[(j, k)] == y[(j,k)] +  quicksum(x[(i,j)] * pt[i][k] for i in index_i) for j in range(1,n) for k in range(1, m) ), name ="cons6")
 
    for i in range(n):
        model.addConstr(sum(x[(i,j)] for j in range(n)) == 1)
    for j in range(n):
        model.addConstr(sum(x[(i,j)] for i in range(n)) == 1)
        


	# auto-tune the parameters
#    m.tune()

	# optimize!
    model.optimize()
#    model.computeIIS()
#    model.write("model.lp")

	
	# print out the objective function value
    print('Obj: %g' % model.objVal)
    vars =  model.getVars()
    for i in range(25):
        if(vars[i].x == 1):
         print('%s %g' % (vars[i].varName, vars[i].x))
#    for i in range(10, 35):
#        if(vars[i].x == 1):
#            print('%s %g' % (vars[i].varName, vars[i].x))

#	# print out the schedules
#    for i in index_i:
#        for j in pos_j:
#            if(x[(i,j)] == 1 ):
#                    print (i, j, x[(i,j)])                    
            
# : exceptions :
except GurobiError as e:
	print('Error code ' + str(e.errno) + ": " + str(e))

except AttributeError:
	print('Encountered an attribute error')