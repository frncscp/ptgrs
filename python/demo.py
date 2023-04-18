from Ptgrs import Ptgrs
from mpmath import mp, mpf #for big decimal numbers
import matplotlib.pyplot as plt #graphing
while True:
    choice = input(f"{'*'*10}PTGRS{'*'*11}\n****github.com/frncscp****\n{'*'*26}\n\nThis program answers to the following questions:\nWhat is the difference between the hypotenuse and the longest leg of a\nright triangle that is the smallest (empirically possible) to find?\nWhat would the graph look like?\n\nBy looping throung a set of right triangles, it will store the difference\nbetween the long leg and the hypotenuse.\n\nChoose you option:\n1)Choose range and triangle sides' length.\n2)Choose the tiny leg's length and it's substraction per loop.\n(Any other option will close the program.)\n(If you get a minimum difference of 0, try to run the program again with a bigger range.)\n\nType here: ")
    if choice != '1' and choice != '2':
        break
    elif choice == '1':
        print('Option 1 has been chosen')
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
            print(f'Loading: {round((i/rango)*100,2)}%', end = '\r')
            if triang.h == triang.c1 == triang.c2:
                triang.c2-resta
            if triang.check(): #if the triangle actually is a right triangle
                triangs.append({'hptns': triang.h, 'c1': triang.c1, 'c2': triang.c2})
                triang.c2 -= resta #substracts var
                difftotal.append(triang.h - triang.c1) #saves the difference to a list
                x.append(i) #adds consecutive numbers to a list
                c.append(0) #adds zeros
            triang.pitagorazo('h')
        scale = 10**resta
    elif choice == '2':
        print('Option 2 has been chosen')
        #my variable type check system: put all the values into a dictionary and iterate it to check all value types
        vars = {
            'substract' : input('Type the number that will be substracted from the tiny leg: '),
            'leg2' : input('Type the value for the tiny leg: ' )
        }
        #basically the program lets the user choose a value for the tiny leg length and another one for the value
        # that will be substracted per loop, then when all the values can be converted to float they are changed
        for label, value in vars.items():
            while mpf(vars[label]) == False:
                vars[label] = input(f'Wrong data type on {label} type\nTry Again: ')
            vars[label] = mpf(vars[label])
        while vars['leg2'] < vars['substract']*3: #while the tiny leg is less than three times the substract value (for the graph)
            vars['leg2'] = input(f'Insufficient value for leg length, the minimum value possible is {3*vars["substract"]}\nTry again: ')
            while mpf(vars['leg2']) == False:
                vars['leg2'] = input(f'Wrong data type on leg2 type\nTry Again: ')
            vars['leg2'] = mpf(vars['leg2'])   
        triang = Ptgrs(vars['leg2'], vars['leg2'], vars['leg2']) #Ptgrs class var, 
        #as the program just asked for one leg, let the triangle have two equal legs, same with the hypotenuse
        triang.pitagorazo('h') #to make an actual right triangle
        rango = triang.c2/vars['substract']#tiny leg divided by the substract value is the same as the range
        #i used the range for the basic program, as this doesn't use range, i just cleared the equation
        mp.dps = round(mp.ln(rango)/2) 
        difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
        x = [] #x axis
        c = [] #full of zeros (for comparisons)
        triangs = []
        for i in range(round(rango)):
            print(f'Loading: {round((i/rango)*100,2)}%', end = '\r')
            if triang.h == triang.c1 == triang.c2:
                triang.c2-vars['substract']
            if triang.check(): #if the triangle actually is a right triangle
                triangs.append({'hptns': triang.h, 'c1': triang.c1, 'c2': triang.c2})
                triang.c2 -= vars['substract'] #substracts var
                difftotal.append(triang.h - triang.c1) #saves the difference to a list
                x.append(i) #adds consecutive numbers to a list
                c.append(0) #adds zeros
            triang.pitagorazo('h')
        scale = 10**vars['substract']
    aux = 0
    tiniest_diff = difftotal[-3]
    for item in difftotal: #looping through the list
        item*= scale #multiply by the scale so i have integer numbers (better for efficiency while graphing)
        difftotal[aux] = item #add the scaled item to the list
        aux+=1 #for accessing to the indexes
    print(f'The minimum difference between the hypotenuse and the long leg of all right triangles was: {tiniest_diff}.') 
    #the last but one number of the list, before zero, is the minimum difference between the hypotenuse and long leg 
    plt.title('Limit of difference between the hypotenuse and the long leg of a right triangle.')
    plt.ylabel('Leg-hypotenuse difference')
    plt.plot(x, difftotal) #graph
    plt.plot(x, c) #plain graph with y = 0
    plt.show()
    choice = input('If you wish to execute a new task, press 1.\nOtherwise, press any key.\nType here: ')
    if choice == '1':
        continue
    else: 
        break