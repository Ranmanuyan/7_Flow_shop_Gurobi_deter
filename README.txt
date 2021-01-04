Codes wrote by Lei Liu 
POLIMI, ITALY



-----------------------------------------------------------------------
DeterFlowShopTar.py
12, Jun, 2020 

This is a flow shop scheduling with total tardiness minimization.
Deterministic Version
The classical tardiness calculation model for flow shop scheduling

The Processing time is given and deterministic.
Use python and Gurobi to solve it.
The model is in the Research Notes Book for reference
				- DAILYIMPORTANTACCUMULATION  
				- 1.3.5 Calculation of total tardiness in flow shop scheduling

-----------------------------------------------------------------------
FS_tar_ reentrance.py
3 July 2020
deterministic

This is a flow shop scheduling with total tardiness minimization with two machines(deterministic) need to be re-entered.
modify the classical tardiness model:
1, transform it as a flow shop with bypass
2, add the disjunctive constraints
3, add starttime and Y_ij binary variables



-----------------------------------------------------------------------

15 Sep 2020
getObjfromShedule

have a known schedule, calculate its obj, such as total completion time. with disjunctive constraints/ or half disjunctive constraints .



-----------------------------------------------------------------------
15 Sep 2020
location_Schedule.py
Flow shop folder

transform from a location list to schedule list



-----------------------------------------------------------------------
optimal_for_scenario.py

given a new scenario, calculate the optimal schedule and total completion time
pay attention to the disjunctive constraints, 




