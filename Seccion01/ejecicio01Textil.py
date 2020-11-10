from gurobipy import *

# define constant
looms = ["Jacquard", "Ratier", "outside"]
inside_loom = ["Jacquard", "Ratier"]
capty = {"Jacquard": 8, "Ratier": 30}
fabrics = [1, 2, 3, 4, 5]
fabrics_x = {
    "Jacquard": {1: 4.63, 2: 4.63, 3: 5.23, 4: 5.23, 5: 4.17},
    "Ratier": {1: -1, 2: -1, 3: 5.23, 4: 5.23, 5: 4.17}
}

demands_fabric = {1: 16500, 2: 22000, 3: 62000, 4: 7500, 5: 62000}
hr = 24
days = 30

sale_price = {1: 3.99, 2: 3.86, 3: 4.10, 4: 4.24, 5: 3.70}
costs = {
    "Jacquard": {1: 2.66, 2: 2.55, 3: 2.49, 4: 2.51, 5: 2.50},
    "Ratier": {1: 2.66, 2: 2.55, 3: 2.49, 4: 2.51, 5: 2.50},
    "outside": {1: 2.86, 2: 2.70, 3: 2.60, 4: 2.70, 5: 2.70}
}
# set name Model
model = Model("Textil")

# add decision variable

desicion_var = model.addVars(fabrics, looms, vtype=GRB.CONTINUOUS, name="meter of frabic i on j loom")

# add constraint(s)
model.addConstr(desicion_var[1, "Ratier"] == 0)
model.addConstr(desicion_var[2, "Ratier"] == 0)

model.addConstrs(
    quicksum(desicion_var[fabr, loom] for loom in looms) >= demands_fabric[fabr]
    for fabr in fabrics)

model.addConstrs(
    quicksum(desicion_var[fabr, loom] /
             (fabrics_x[loom][fabr] ) for fabr in fabrics)
    <= capty[loom] * hr * days for loom in inside_loom
)
# model.addConstr(
#     quicksum(desicion_var[fabr, "Ratier"]/(fabrics_x["Ratier"][fabr] ) for fabr in range(3,6))
#     <= capty["Ratier"]* hr * days
# )


# define Objetive

funtion_objetive = quicksum(
     (costs[loom][fabr])*desicion_var[fabr, loom]
    for fabr in fabrics for loom in looms
)
model.setObjective(funtion_objetive, GRB.MINIMIZE)
# write model in a file
model.write("textil.lp")
for x in fabrics:
    for y in looms:
        print(desicion_var[x, y])
        print(sale_price[x])
        print(costs[y][x])
# calcule solution
model.optimize()
# print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())

