from mpmath import mp, mpf #me permite usar decimales arbitrariamente exactos
import matplotlib.pyplot as plt #gráfico
from itertools import count #para rellenar los números en x dentro del gráfico
rango = int(input('Inserte rango: ')) #número de iteraciones, con 1000 pueden ser suficientes
mp.dps = int(input('Inserte número de decimales: ')) #cuántos decimales máximos se usarán en las operaciones, si son pocos no funciona
indice = count()
class Ptgrs:
    def __init__(self, h, c1, c2): #hipotenusa, catetos
        self.h = h
        self.c1 = c1
        self.c2 = c2
    def check(self): #saber si se cumple el teorema de pitágoras
        return self.h%((self.c1**2)+(self.c2**2))**0.5 < 0.05
    def pitagorazo(self, lado): #aplicar teorema por despeje
        if lado == 'h':
            self.h = ((mpf(self.c1**2)) + mpf(self.c2**2))**0.5
            return self.h
        elif lado == 'c1':
            self.c1 = ((self.h**2) - (self.c2**2))**0.5
            return self.c1
        elif lado == 'c2':
            self.c2 = ((self.h**2)-(self.c1**2))**0.5
            return self.c2   
h = int(input('Ingrese el valor de la hipotenusa: ')) 
c = int(input('Ingrese el valor de un cateto: '))
cc = int(input('Ingrese el valor del otro cateto: ' ))
if c>cc: # si c es mayor a cc, que c sea el cateto mayor, y viceversa
  c1 = c
  c2 = cc
elif cc > c:
  c1 = cc
  c2 = c
triang = Ptgrs(h, c1, c2) #variable de la clase Ptgrs
resultado = open('Resultado.txt', 'w') #guardar cada diferencia en un archivo de texto
resta = triang.c2/rango #decide cuánto va a restar al cateto pequeño en cada iteración, ej: 2cm/100 = 0.02
difftotal = [] #todas las diferencias entre cateto e hipotenusa por cada iteración, luego servirá para graficar en y
x = [] #x
c = [] #lista llena de ceros para hacer comparación entre gráficas
for i in range(rango):
    if triang.check(): #si cumple el teorema
        print(triang.h, triang.c1, triang.c2)
        triang.c2 = mpf(str(triang.c2)) - mpf(str(resta)) #resta el número deducido
        triang.pitagorazo('h') #ejecuta teorema
        difftotal.append(mpf(str(triang.h)) - triang.c1) #guarda la diferencia
        x.append(next(indice)) #agrega el número consecutivo en la lista x
        c.append(0) #agrega el 0 en lista c
    if triang.check() == False: #si no cumple el teorema
        triang.pitagorazo('h') #ejecuta teorema
    if mpf(str(triang.h)) - triang.c1 <= 0: #si la diferencia cateto hipotenusa es menor o igual a 0, acabar loop
        break
mindiff = difftotal[-2] #el penúltimo valor de la lista, antes de cero, es la diferencia mínima
j = 0
for item in difftotal: #iterando a través de la lista
    resultado.write(f'{j+1}.) {str(item)}\n') #guardo elementos en el txt
    item*= 10 #multiplico por diez para que la escala sea más cómoda
    difftotal[j] = item #lo agrego de nuevo a la lista para poder usar el número escalado
    j+=1 #para llevar la cuenta de cada iteración en el txt
print(f'La diferencia mínima alcanzada entre el cateto mayor y la hipotenusa fue de: {mindiff}.')
plt.title('Límite de diferencia entre cateto e hipotenusa de un triángulo rectángulo.')
plt.ylabel('Diferencia Cateto-Hipotenusa')
plt.plot(x, difftotal) #gráfica de la diferencia
plt.plot(x, c) #gráica de la recta en y=0
plt.savefig('pitagorazofinal.png')
plt.show()