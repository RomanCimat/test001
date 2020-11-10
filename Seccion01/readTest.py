from gurobipy import *
model = Model("algo")
model.read("Investment_min_risk.lp")
model.optimize()

