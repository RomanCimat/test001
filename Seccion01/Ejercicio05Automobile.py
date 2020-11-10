from gurobipy import *

# define constant
automobiles = ["sedan","trocas"]
paints = [2000,1500]
assamble=2200
profit = [2100, 3000]

# set name Model
model = Model("Automobil industry")

# add decision variable

desicion_vars = model.addVars(automobiles, lb=0, vtype=GRB.CONTINUOUS, name="number of cars")
# add constraint(s)

# model.addConstr((desicion_vars["saloon"]/paints[0]) + (desicion_vars["carrier"]/paints[1]) <= 1)
model.addConstr(quicksum(desicion_vars[automobiles[i]]/paints[i] for i in range(len(automobiles))) <= 1)

model.addConstr(quicksum(desicion_vars[automobiles[i]] for i in range(len(automobiles))) <= assamble)
# define Objetive
funtion_objetive = quicksum(profit[i]*desicion_vars[automobiles[i]] for i in range(len(automobiles)))
model.setObjective(funtion_objetive, GRB.MAXIMIZE)
# write model in a file
model.write("industryAutomobil.lp")
# calcule solution
model.optimize()
# print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())
