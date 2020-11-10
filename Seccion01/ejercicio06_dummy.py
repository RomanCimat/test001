from gurobipy import *
chance_investment = 4
max_investment=200000
return_expected = 0.09
limit_single_investment = 0.5

companies=["telefonita","sankander","ferrofial","gamefal"]
price_per_share = [100, 50, 80, 40]
anual_rate_return = [0.12,0.08, 0.06,0.1]
risk = [0.1, 0.07, 0.05, 0.08]

#crear modelo
model = Model("Investment")
# variables de decision

decision_var = model.addVars(companies, vtype=GRB.CONTINUOUS, name="number_shares_of_i")
#añadir restricciones
total_invest = quicksum(price_per_share[index] * decision_var[companies[index]] for index in range(len(companies)))
model.addConstr( total_invest <= max_investment)
model.addConstr(
    quicksum(anual_rate_return[index] * price_per_share[index] * decision_var[companies[index]] for index in range(len(companies))) >=
    return_expected * max_investment
)

model.addConstrs(
    price_per_share[i] * decision_var[companies[i]] <=
    limit_single_investment * total_invest for i in range(len(companies))
)


#inciso A
func_obj_risk= quicksum(risk[i] * price_per_share[i] * decision_var[companies[i]] for i in range(len(companies)))
func_obj_return= quicksum(anual_rate_return[i] * price_per_share[i] * decision_var[companies[i]] for i in range(len(companies)))

model.setObjective(func_obj_risk, GRB.MINIMIZE)

model.write("Investment_min_risk.lp")

model.optimize()
print("MODELO A")
if model.SolCount > 0:
    model.printAttr("x")
    print("risk: %g" % func_obj_risk.getValue())
    print("return: %g" % func_obj_return.getValue())
    print("total investmente: %g" % total_invest.getValue())
    print("falla prob risk: %g" % (func_obj_risk.getValue()/total_invest.getValue()))

#inciso B
model.setObjective(func_obj_return, GRB.MAXIMIZE)

model.write("Investment_max_return.lp")
model.optimize()
print("MODELO B")
if model.SolCount > 0:
    model.printAttr("x")
    print("risk: %g" % func_obj_risk.getValue())
    print("return: %g" % func_obj_return.getValue())
    print("total investmente: %g" % total_invest.getValue())
    print("falla prob risk: %g" % (func_obj_risk.getValue() / total_invest.getValue()))

