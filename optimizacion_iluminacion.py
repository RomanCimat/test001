from gurobipy import *
opt_modelo= Model("Compras de lamparas")
modelos_lamparas = ["mercurio125", "sodio150", "sodio250", "led100"]
costo_por_unidad = [275,300,360,1715.5]
costo_luz=[294932016000,353918419200,589864032000,235945612800]
unidades_fallidas = 2110
presupuesto = 25000000000000
unidades_compradas = opt_modelo.addVars(modelos_lamparas, vtype=GRB.INTEGER, name="numero de unidades")


opt_modelo.addConstr(quicksum(unidades_compradas[modelos_lamparas[i]] for i in range(len(modelos_lamparas))) == unidades_fallidas)

objetivo_sin_luz = quicksum(costo_por_unidad[i]*unidades_compradas[modelos_lamparas[i]] for i in range(len(modelos_lamparas)))

objetivo_con_luz = quicksum((costo_luz[i]+costo_por_unidad[i])*unidades_compradas[modelos_lamparas[i]] for i in range(len(modelos_lamparas)))

opt_modelo.setObjective(objetivo_sin_luz, GRB.MINIMIZE)

opt_modelo.write("comprasSinLuz.lp")
opt_modelo.optimize()
print("compras Sin Luz")
if opt_modelo.SolCount > 0:
    opt_modelo.printAttr("x")
    print("f: %g" % objetivo_sin_luz.getValue())
opt_modelo.addConstr(objetivo_con_luz <= presupuesto)
opt_modelo.setObjective(objetivo_con_luz, GRB.MINIMIZE)
opt_modelo.write("comprasConLuz.lp")
opt_modelo.optimize()
print("compras Con Luz")
if opt_modelo.SolCount > 0:
    opt_modelo.printAttr("x")
    print("f: %g" % objetivo_con_luz.getValue())