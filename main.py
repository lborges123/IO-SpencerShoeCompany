import pulp
import header

#DADOS

val = header.readArrayFromFile('productvalue.txt') #Valor unitario dos produtos
cap = header.readArrayFromFile('factcapacity.txt') #Capacidade das fabricas
usage = header.readMatrixFromFile('usageresources.txt') #Uso de recursos para produzir produto i na fabrica j
totalcap = header.readIntegerFromFile('limitetotal.txt') #Capacidade agregada das fabricas

#CONJUNTOS

Prod = range(0,len(val)) #produtos
Fab = range(0,len(cap)) #fabricas

#VARIAVEIS DE DECISAO
x = pulp.LpVariable.dicts('x',[(i,j) for i in Prod for j in Fab],cat=pulp.LpInteger,lowBound=0) #Quantidade produzida de produto i na fabrica j
y = pulp.LpVariable.dicts('y',Fab,cat=pulp.LpBinary) #Se a fabrica j e usada ou nao

#CRIAR MODELO
modelo = pulp.LpProblem('producao', pulp.LpMaximize)

#FUNCAO OBJETIVO
modelo += sum(val[i]*x[(i,j)] for i in Prod for j in Fab)

#RESTRICOES
modelo += sum(usage[i][j]*x[(i,j)] for i in Prod for j in Fab) <= totalcap, 'LimiteTotal'

for j in Fab:
  modelo += sum(usage[i][j]*x[(i,j)] for i in Prod) <= cap[j]*y[j],'LimiteCapacidade_{}'.format(j)

modelo += sum(y[j] for j in Fab) <= 2, 'MaxFabricas'

#RESOLVER
status=modelo.solve() 

if status==pulp.LpStatusOptimal:
  print (modelo.objective.value()) #imprime valor FO otimo na janela de output
  for i in Prod:
    for j in Fab:
      print(x[(i,j)],x[(i,j)].varValue) #imprime nome da variavel x e seu valor na solucao otima na janela de output
  for j in Fab:
    print(y[j],y[j].varValue) #imprime nome e valor no otimo da variavel y
  modelo.writeLP('mylp') #cria ficheiro LP do modelo