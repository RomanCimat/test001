from gurobipy import *

# define constant
machines= 2
cost_minutes =[10,5]
capacity = [500,380]
production = [[2,3,4,2],
              [3,2,1,2]]
products= 4
sale_price=[65,70,55,45]
# set name Model
model = Model("Metallurgica company")

# add decision variable

desicion_vars = model.addVars(products,vtype=GRB.CONTINUOUS, name="number of product i")

# add constraint(s)
model.addConstrs(quicksum(desicion_vars[i]*production[j][i] for i in range(products))<= capacity[j] for j in range(machines))
# define Objetive
cost_prod_m1 = quicksum(cost_minutes[0] * production[0][i] * desicion_vars[i] for i in range(products))
cost_prod_m2 = quicksum(cost_minutes[1] * production[1][i] * desicion_vars[i] for i in range(products))
price_production= quicksum(sale_price[i]*desicion_vars[i] for i in range(products))
funtion_objetive = price_production - cost_prod_m1 - cost_prod_m2
model.setObjective(funtion_objetive, GRB.MAXIMIZE)
# write model in a file
model.write("metallurigical.lp")
# calcule solution
model.optimize()
# print solution
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % funtion_objetive.getValue())
