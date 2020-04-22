# -*- coding: utf-8 -*-
"""
@author: Hemant
"""
from itertools import product
from math import sqrt

import gurobipy as gp
from gurobipy import GRB
from gurobipy import *

#'locations' of the requests in X-Y coordinate space first row are the X coordinates, and 2nd row the Y So (15,54) is the location of the first request and they are ordered by increasing X value 
reqLocations = [(15,54), (17,23), (19,77), (25,7), (29,73), (29,87), (32,40), (37,17), (44,57), (44, 61), (58,12), (58, 35), (68,87), (73,65), (80,17), (80,50), (82,73) ]      
ViProfit = [60,40,90,30,100,110,70,50,100,100,70,90,150,130,90,130,150]

#'locations' of the possible pool configurations in the same X-Y space (100,100) is the top right, and so 100 is the maximum request for either X or Y
poolLocations = [(20, 20),(20, 50),(20, 80), (50, 20), (50, 50), (50, 80), (80, 20), (80, 50), (80, 80), (100, 100)]
poolCapacity = [1,1,2,2,3,3,3,3,4,4]
costJ =  [3,3,5,5,6,6,6,6,8,10]

def compute_distance(loc1, loc2):
    if loc1[0] <= loc2[0] and loc1[1] <= loc2[1]:
        dx = loc2[0] - loc1[0]
        dy = loc2[1] - loc1[1]
    else:
        dx = -1
        dy = -1
    return (dx + dy)

numRequests = len(reqLocations)
numPools = len(poolLocations)
#cartesian_prod = list(product(range(numRequests), range(numPools)))
#print(cartesian_prod)
#costPerDifference=1

xjp= tuplelist() #variable for job assignments to pool  

# creating list of valid tuples where resources are more than demand Xij binary variable for pool assignment    
for j in range(numRequests):
    for p in range(numPools):
        if reqLocations[j][1]<=poolLocations[p][1] and reqLocations[j][0]<=poolLocations[p][0]:
            xjp.append((j,p))

print(xjp)

m = Model('Pool Creation')
assign = m.addVars(xjp, vtype=GRB.BINARY, name='Assign') 

"""
#minimize resource waste (w)
m.modelSense = GRB.MINIMIZE
m.setObjective(quicksum(compute_distance(reqLocations[i[0]],poolLocations[i[1]])*assign[i] for i in xjp)) 
"""

#maximize Value (v-w-c)

m.modelSense = GRB.MAXIMIZE
m.setObjective(quicksum(assign.sum('*',p) * ViProfit[p] for p in set([k[1] for k in xjp]))\
                   -quicksum(compute_distance(reqLocations[i[0]],poolLocations[i[1]])*assign[i] for i in xjp)\
                   -quicksum(assign.sum('*',p)* costJ[p]  for p in set([i[1] for i in xjp])))



m.addConstrs((assign.sum(j,'*') == 1 for j in range(numRequests)), name='PoolAssign')

m.addConstrs((assign.sum('*',p) <= poolCapacity[p] for p in set([i[1] for i in xjp] )), name='PoolCapacity') 

m.optimize()

for allocation in xjp:
    if assign[allocation].X>0.00000000001:
        print(allocation)









#reqLocations = [[15,17,19,25,29,29,32,37,44,44,58,58,68,73,80,80,82],
#				[54,23,77,7,73,87,40,17,57,61,12,35,87,65,17,50,73]]
#poolLocations = [[20,20,20,50,50,50,80,80,80,100],
#				  [20,50,80,20,50,80,20,50,80,100]]
#lambdaJ = [1,1,2,2,3,3,3,3,4,4]
#numPools = 10;          #number of pools
#numRequests = 17;       #number of requests
#maintenance = 100;		#common maintenance cost per pool

#capacity = 5;			#capacity of each pool
#wastage = {(r,p): costPerDifference*compute_distance(reqLocations[r], poolLocations[p]) for r, p in cartesian_prod}

"""
select = m.addVars(numPools, vtype=GRB.BINARY, name='Select')

assign = m.addVars(cartesian_prod, ub=1, vtype=GRB.CONTINUOUS, name='Assign')

m.addConstrs((assign[(r,p)] <= select[p] for r,p in cartesian_prod), name='PoolAssign')
m.addConstrs((gp.quicksum(assign[(r,p)] for p in range(numPools)) == 1 for r in range(numRequests)), name='Demand')
m.setObjective(assign.prod(wastage), GRB.MINIMIZE)

m.write('testpool.lp')
"""
#m.optimize()




""" wijPool = [[0 for x in range(numPools)] for y in range(numRequests)] 
xijPools = [[0 for x in range(numPools)] for y in range(numRequests)]

for req in range(numRequests-1):
	for pool in range(numPools-1):
		if reqLocations[0][req] <= poolLocations[0][pool] and reqLocations[1][req] <= poolLocations[1][pool]:
			wijPool[req][pool] = (poolLocations[0][pool] - reqLocations[0][req]) + (poolLocations[1][pool] - reqLocations[1][req])
			xijPools[req][pool] = 1
		else:
			wijPool[req][pool] = 0
			xijPools[req][pool] = 0
print(xijPools)
print(wijPool)
    

cj =  [3,3,5,5,6,6,6,6,8,8]
vi = [6,4,9,3,10,11,7,5,10,10,7,9,15,13,9,13,15]
idxReq = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
"""

"""
model = Model('Pool Creation')

#Variables

totalServed = model.addVars(numPools, name="totalServed")
poolUsed = model.addVars(numPools, vtype=GRB.BINARY, name="poolUsed")
#print(poolUsed)
itemAccepted = model.addVars(numRequests,vtype=GRB.BINARY, name="itemAccepted")
#print(itemAccepted)
#allocation = model.addVars(numRequests, numPools,vtype=GRB.BINARY, obj=lmdj, name="allocation")
allocation = model.addVars(numRequests, numPools,vtype=GRB.BINARY, obj=xijPools, name="allocation")
#print(allocation)
waste = model.addVars(numRequests, numPools, obj=wijPool, name="waste")
#print(waste)

model.modelSense = GRB.MINIMIZE

#Constraints

model.addConstrs((sum(xijPools[i])<=1 for i in range(numRequests-1)),name="onePool")
#model.addConstrs((allocation[i]<=1 for i in range(numRequests-1)),name="allocation")

model.setObjective(quicksum(xijPools[i][j] * wijPool[i][j]  for i in range(numRequests-1) for j in range(numPools-1)))

model.write('testpool.mps')
model.optimize()
"""