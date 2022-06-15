from main import Ptgrs
from mpmath import mp, mpf #for big decimal numbers
import matplotlib.pyplot as plt #graphing

#my variable type check system: put all the values into a dictionary and iterate it to check all value types
vars = {
    'range' : input('Type range: '),
    'hypotenuse' : input('Type the value for the hypotenuse: '),
    'leg1' : input('Type the value for one leg: '),
    'leg2' : input('Type the value for the other leg: ' )
}

#if something's wrong it can be changed directly onto the dict and later assigned on the variable
for label, value in vars.items():
    while vars[label].isnumeric() == False:
        vars[label] = input(f'Wrong data type on {label} type\nTry Again: ')

rango = int(vars['range'])
h = int(vars['hypotenuse'])
c = int(vars['leg1'])
cc = int(vars['leg2'])

mp.dps = round(mp.ln(rango)/2) 
#a logarithmic function decreases its growth while the x value goes up, so its useful to assign the number of 
# decimal values without getting big numbers


if c>cc: # deciding which var will be the longest leg
    c1, c2 = c, cc
elif cc > c:
    c1, c2 = cc, c
elif c == cc:
    c1, c2 = c, cc

triang = Ptgrs(h, c1, c2) #Ptgrs class var
resta = mpf(triang.c2/rango) #decides how much the tiny leg will be shrinked per loop, ej: 2cm/100Loops = 0.02
difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
x = [] #x axis
c = [] #full of zeros (for comparisons)
triangs = [] #it gives access to any given triangle (h, c1, c2)
aux = 0

for i in range(rango):
    print(f'Cargando: {round((i/rango)*100,2)}%', end = '\r')
    if triang.h - triang.c1 == 0:
        break
    if triang.check(): #si cumple el teorema
        triangs.append({'hptns': triang.h, 'c1': triang.c1, 'c2': triang.c2})
        triang.c2 -= resta #resta el número deducido
        difftotal.append(triang.h - triang.c1) #guarda la diferencia
        x.append(i) #agrega el número consecutivo en la lista x
        c.append(0) #agrega el 0 en lista c
    triang.pitagorazo('h')

scale = 10**resta
aux = 0

for item in difftotal: #iterando a través de la lista
    item*= scale #multiplico por diez para que la escala sea más cómoda
    difftotal[aux] = item #lo agrego de nuevo a la lista para poder usar el número escalado
    aux+=1 #para llevar la cuenta de cada iteración en el txt

print(f'La diferencia mínima alcanzada entre el cateto mayor y la hipotenusa fue de: {difftotal[-2]/scale}.') 
#the last but one number of the list, before zero, is the minimum difference between the hypotenuse and long leg 

plt.title('Limit of difference between the hypotenuse and the long leg of a rectangle triangle.')
plt.ylabel('Leg-hypotenuse difference')
plt.plot(x, difftotal) #graph
plt.plot(x, c) #plain graph with y = 0
plt.show()