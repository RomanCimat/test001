from gurobipy import *

# define constant
products =["GCA", 'GCB','GCC']
sale_price =[125,135,155]
demands=[6000,7000,9000]
crit_ratio=0.3
components = ['C1', 'C2']
comp_avail = [10000, 15000]
crit_elem_c1 = 0.4
crit_elem_c2 = 0.2
# set name Model
model = Model("Cosmetic Firm")

# add decision variable

desicion_vars = model.addVars(components, products, vtype=GRB.CONTINUOUS, name="litresOf i On j")

# add constraint(s)
#availability
model.addConstrs( quicksum(desicion_vars[components[i],products[j]] for j in range(len(products))) <= comp_avail[i] for i in range(len(components)) )
#demand
model.addConstrs(
    quicksum(desicion_vars[components[i],products[j]] for i in range(len(components))) >= demands[j]
    for j in range(len(demands))
)
#ratio
model.addConstr(
    crit_elem_c1*desicion_vars["C1","GCA"] + crit_elem_c2*desicion_vars["C2","GCA"] >=
    crit_ratio*(desicion_vars["C1","GCA"] + desicion_vars["C2","GCA"])
)
model.addConstr(
    crit_elem_c1 * desicion_vars["C1","GCB"] + crit_elem_c2 * desicion_vars["C2","GCB"] <=
    crit_ratio * (desicion_vars["C1","GCB"] + desicion_vars["C2","GCB"])
)
model.addConstr(
    desicion_vars["C1","GCC"] >= crit_ratio * desicion_vars["C2","GCC"]
)

# define Objetive
funtion_objetive = quicksum(
    sale_price[j] * quicksum(
        desicion_vars[components[i],products[j]] for i in range(len(components))
    ) for j in range(len(products))
)
model.setObjective(funtion_objetive, GRB.MAXIMIZE)
# write model in a file
model.write("cosmeticFirm.lp")
# calcule solution
model.optimize()
# print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())
