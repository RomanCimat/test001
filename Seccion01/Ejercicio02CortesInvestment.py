from gurobipy import *

# define constant
years = 6
requir = {3: 20000, 4: 22000, 5: 24000, 6: 26000}
invs = ["A", "B", "C", "D"]
profit = {"A": 0.05, "B": 0.13, "C": 0.28, "D": 0.40}
maturity = [1, 2, 3, 4]
# set name Model
model = Model("Cortes Investments")

# add decision variable or list(range(1,n))
desicion_Vars = model.addVars(invs, range(1, years), vtype=GRB.CONTINUOUS, name="amount dolars in i in the year j")
# add constraint(s)
model.addConstr(desicion_Vars["D", 3] == 0)
model.addConstr(desicion_Vars["D", 4] == 0)
model.addConstr(desicion_Vars["C", 4] == 0)
model.addConstr(desicion_Vars["D", 5] == 0)
model.addConstr(desicion_Vars["C", 5] == 0)
model.addConstr(desicion_Vars["B", 5] == 0)
# first year
model.addConstr(
    (1 + profit["A"]) * desicion_Vars["A", 1]
    ==
    quicksum(desicion_Vars[inv, 2] for inv in invs))
# second year
model.addConstr(
    (1 + profit["A"]) * desicion_Vars["A", 2] +
    (1 + profit["B"]) * desicion_Vars["B", 1]
    ==
    quicksum(desicion_Vars[inv, 3] for inv in invs) + requir[3])
# end third year start fourth year
model.addConstr(
    (1 + profit["A"]) * desicion_Vars["A", 3] +
    (1 + profit["B"]) * desicion_Vars["B", 2] +
    (1 + profit["C"]) * desicion_Vars["C", 1]
    ==
    quicksum(desicion_Vars[inv, 4] for inv in invs) + requir[4])
# forth year
model.addConstr(
    (1 + profit["A"]) * desicion_Vars["A", 4] +
    (1 + profit["B"]) * desicion_Vars["B", 3] +
    (1 + profit["C"]) * desicion_Vars["C", 2] +
    (1 + profit["D"]) * desicion_Vars["D", 1]
    ==
    quicksum(desicion_Vars[inv, 5] for inv in invs) + requir[5])
# 5°
model.addConstr(
    (1 + profit["A"]) * desicion_Vars["A", 5] +
    (1 + profit["B"]) * desicion_Vars["B", 4] +
    (1 + profit["C"]) * desicion_Vars["C", 3] +
    (1 + profit["D"]) * desicion_Vars["D", 2]
    ==
    requir[6])
# 20%

# model.addConstr(
#     0.8*quicksum(desicion_Vars["C",i] + desicion_Vars["D",i] for i in range(1,years)) <=
#     0.2*quicksum(desicion_Vars["A", i] +desicion_Vars["B",i] for i in range(1,years))
# )
model.addConstrs(
    0.8 * desicion_Vars["C", i] + desicion_Vars["D", i] <=
    0.2 * desicion_Vars["A", i] + desicion_Vars["B", i] for i in range(1, years)
)
# define Objetive
funtion_objetive = quicksum(desicion_Vars[inv, 1] for inv in invs)
model.setObjective(funtion_objetive, GRB.MINIMIZE)
# write model in a file
model.write("CortesInvestment.lp")
# calcule solution
model.optimize()
# print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())
