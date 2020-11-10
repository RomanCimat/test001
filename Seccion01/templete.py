from gurobipy import *
#define constant

#set name Model
model= Model("Name")

#add decision variable

desicion_Var = model.addVar(... )
desicion_Vars = model.addVars(...)
# add constraint(s)
model.addConstr(...)
model.addConstrs(...)
#define Objetive
funtion_objetive= 0
model.setObjective(funtion_objetive, GRB.)
#write model in a file
model.write("nameFile.lp")
#calcule solution
model.optimize()
#print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())
