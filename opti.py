import random
import numpy as np 
from scipy.stats import norm
import sys


# N cantPersonas
# M cantProyectos
# nameTxt nombre del archivo

cantPersonas = int(sys.argv[1])
cantProyectos = int(sys.argv[2])
nameTxt = sys.argv[3]

# Listas de largo M
presupuesto = []
minHorasProyectoTotal = []

# Matriz NxM 
minHoras = []
costosHora = []

#####################################
### GENERACION VALORES ALEATORIOS ###
#####################################

for i in range(cantPersonas):
    costosHora.append([])
    for j in range(cantProyectos):
        rand = round(random.randint(1, 3))
        costosHora[i].append(rand)


for i in range(cantProyectos):
    rand = round(random.randint(480, 2000))
    presupuesto.append(rand)

#print(presupuesto)

for i in range(cantProyectos):
    rand = round(random.randint(40, 400))
    minHorasProyectoTotal.append(rand)

for i in range(cantPersonas):
    minHoras.append([])
    for j in range(cantProyectos):
        # Se agregan valores aleatorios
        # Para respetar el intervalo [8,32]
        rand = round(random.randint(40, 160))
        minHoras[i].append(rand)


#######################################
### GENERACION STRINGS RESTRICIONES ###
#######################################


# Restricción presupuesto
# Restricción máx de empleados por cantProyectos
# Restricción min de horas del proyecto

restMaxEmpleados = [] # Ejemplo: ['X_0_0 + X_1_0 + X_2_0 + X_3_0 + X_4_0 <= 5', 'X_0_1 + X_1_1 + X_2_1 + X_3_1 + X_4_1 <= 5']
restMinHoras = [] # Ejemplo: ['H_0_0 + H_0_1 + H_0_2 + H_0_3 + H_0_4 >=701.59;', 'H_1_0 + H_1_1 + H_1_2 + H_1_3 + H_1_4 >=493.55;', ...]
restPresupuesto = []

for j in range(cantProyectos):
    string1=""
    string2 = ""
    string3 = ""
    for i in range(cantPersonas):
        if i == cantPersonas-1:
            string1 += f"{round(costosHora[i][j]*minHoras[i][j],2)} * X_{j}_{i}"
            string2 += "X_"+str(j)+"_"+str(i)
            string3 += f"{minHoras[i][j]} * X_" + str(j) + "_"+str(i)
        else:
            string1 += f"{round(costosHora[i][j]*minHoras[i][j],2)} * X_{j}_{i} + "
            string2 += "X_"+str(j)+"_"+str(i)+" + "
            string3 += f"{minHoras[i][j]} * X_" + str(j) + "_"+str(i) + "+"
            
    string1 += f"<= {presupuesto[j]};"
    string2 += " <= 5;"
    string3 += " >= "+ str(minHorasProyectoTotal[j]) +";"
    restPresupuesto.append(string1)
    restMaxEmpleados.append(string2)
    restMinHoras.append(string3)


# Restricción máx cantProyectos por persona
# Restricción máx horas por persona
# Restriccion min horas persona en proyecto

restMaxProyectos = [] # Ejemplo: ['X_0_0 + X_0_1 + X_0_2 + X_0_3 + X_0_4 + X_0_5<= 5', 'X_1_0 + X_1_1 + X_1_2 + X_1_3 + X_1_4 + X_1_5<= 5', ...]
restMaxHoras = []


for i in range(cantPersonas):
    string1 = ""
    string = ""
    string2 = ""
    for j in range(cantProyectos):
        if j == cantProyectos-1:
            string += "X_"+str(j)+"_"+str(i)
            string2 += f"{minHoras[i][j] }* X_{j}_{i}"
        else:
            string += "X_"+str(j)+"_"+str(i)+" + "
            string2 += f"{minHoras[i][j] }* X_{j}_{i} +"
    string += " <= 5;"
    string2 += " <= 160;"
    restMaxProyectos.append(string)
    restMaxHoras.append(string2)


restBinarias = "bin "
for i in range(cantProyectos):
    for j in range(cantPersonas):
        if j == cantPersonas-1 and i == cantProyectos-1:
            restBinarias+= f"X_{i}_{j};"
        else:
            restBinarias+= f"X_{i}_{j},"


########################
### Funcion objetivo ###
########################

funcionObjetivo = "min:"
for i in range(cantProyectos):
    for j in range(cantPersonas):
        if i == 0 and j == 0:
            funcionObjetivo+=f" {minHoras[j][i]}*X_{str(i)}_{str(j)}"
        else:
            funcionObjetivo+=f" + {minHoras[j][i]}*X_{str(i)}_{str(j)}"
funcionObjetivo+=";"

###########################
### Creando archivo txt ###
###########################

archivo = open(nameTxt+".lp", "w")



archivo.write(funcionObjetivo+"\n"+"\n")

for item in restPresupuesto:
    archivo.write(item+"\n")

for item in restMaxEmpleados:
    archivo.write(item+"\n")

for item in restMinHoras:
    archivo.write(item+"\n")

for item in restMaxProyectos:
    archivo.write(item+"\n")

for item in restMaxHoras:
    archivo.write(item+"\n")


archivo.write(restBinarias+"\n")

archivo.close()