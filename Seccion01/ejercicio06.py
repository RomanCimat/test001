from gurobipy import *
model= Model("Investment")
chance_investment = 4
max_investment=200000

numbers_investment = model.addVars(chance_investment, vtype=GRB.CONTINUOUS, name="investment_company")

model.addConstr(
    100*numbers_investment[0]+
    50*numbers_investment[1]+
    80*numbers_investment[2]+
    40*numbers_investment[3] == max_investment
)
model.addConstr(
    0.12*100*numbers_investment[0]+
    0.08*50*numbers_investment[1]+
    0.06*80*numbers_investment[2]+
    0.1*40*numbers_investment[3] >= 0.09*max_investment
)
model.addConstrs(numbers_investment[i]<=0.5*max_investment for i in range(chance_investment))
model.addConstrs(numbers_investment[i]>=0 for i in range(chance_investment))
#inciso A
objetive1=0.1*100*numbers_investment[0]+  0.07*50*numbers_investment[1]+   0.05*80*numbers_investment[2]+   0.8*40*numbers_investment[3]
model.setObjective(objetive1, GRB.MINIMIZE)

model.write("Investment_min_risk.lp")
model.optimize()
print("MODELO A")
if model.SolCount > 0:
    model.printAttr("x")
    print("f: %g" % objetive1.getValue())
# #inciso B
# objetive2=0.12*100*numbers_investment[0]+   0.08*50*numbers_investment[1]+    0.06*80*numbers_investment[2]+    0.1*40*numbers_investment[3]
# model.setObjective(objetive2, GRB.MAXIMIZE)
#
# model.write("Investment_max_return.lp")
# model.optimize()
# print("MODELO B")
# if model.SolCount > 0:
#     model.printAttr("x")
#     print("f: %g" % objetive2.getValue())