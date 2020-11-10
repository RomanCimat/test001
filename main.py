from gurobipy import *
model_AE= Model("Asignacion emplados y trabajo")
clases_profesores = 5
profes = 5
clases = 5

preferences =[[5, 8, 5, 9, 7],
              [7,2,3,6,8],
              [9,10,8,9,8],
              [8,7,9,7,8],
              [6,9,9,10,5]]
profesor_i_en_clase_j = model_AE.addVars(clases_profesores, clases_profesores, vtype=GRB.BINARY, name="profe_clase")


model_AE.addConstrs(quicksum(profesor_i_en_clase_j[i, j] for j in range(profes)) == 1 for i in range(clases))
model_AE.addConstrs(quicksum(profesor_i_en_clase_j[i, j] for i in range(clases)) == 1 for j in range(profes))


objetive_function = quicksum(quicksum(preferences[i][j] * profesor_i_en_clase_j[i, j] for i in range(5)) for j in range(5))
model_AE.setObjective(objetive_function, GRB.MAXIMIZE)

model_AE.write("asignacion.lp")
model_AE.optimize()
if model_AE.SolCount > 0:
    model_AE.printAttr("x")
    print("f: %g" % objetive_function.getValue())