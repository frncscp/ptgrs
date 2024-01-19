import streamlit as st
from Ptgrs import Ptgrs
from mpmath import mp, mpf 
import pandas as pd

st.set_page_config(
    page_title="Pythagoras",
    page_icon="🔺",
    layout="wide")

st.title('Interactive demo of Ptgrs')

st.markdown(f"****github.com/frncscp****\n\n\nThis program answers to the following questions:\nWhat is the *difference* between the hypotenuse and the longest leg of a\nright triangle that is the smallest (empirically possible) to find?\nWhat would the graph look like?\n\nBy looping through a set of right triangles, it will store the difference\nbetween the long leg and the hypotenuse.\n\nChoose you option:\n")

#left, right = st.columns(2)

st.caption("(If you get a minimum difference of 0, try to run the program again with a bigger range.)")
left, right = st.columns(2)

status = None

difftotal, x, c, scale = None, None, None, None

def return_results(difftotal, x, c, scale):
    aux = 0
    tiniest_diff = difftotal[-3]
    for item in difftotal: #looping through the list
        item*= scale #multiply by the scale so i have integer numbers (better for efficiency while graphing)
        difftotal[aux] = item #add the scaled item to the list
        aux+=1 #for accessing to the indexes
    st.success(f'The minimum difference between the hypotenuse and the long leg of all right triangles was: {tiniest_diff}.') 
    chart_data = pd.DataFrame(
   {
       "Iterations": x,
       "Hypothenuse - Long leg": difftotal,
       "y = 0": c,
   }
)

    chart_data['Hypothenuse - Long leg'] = chart_data['Hypothenuse - Long leg'].apply(lambda x: float(x))

    
    #the last but one number of the list, before zero, is the minimum difference between the hypotenuse and long leg 
    #plt.title('Limit of difference between the hypotenuse and the long leg of a right triangle.')
    #plt.ylabel('Leg-hypotenuse difference')
    #plt.plot(x, difftotal) #graph
    st.line_chart(chart_data, x="Iterations", y= ["Hypothenuse - Long leg", "y = 0"], use_container_width= False)
    #plt.plot(x, c) #plain graph with y = 0
    #plt.show()

def draw_left_column():
    global status, difftotal, x, c, scale
    with left:
        done_left = False
        if st.button("1) Choose range and triangle sides' length.", key = 'l', type = 'primary'):
            done_left = True
            status = 'L'
        rango_1 = st.number_input('Type range:', value = 0, step = 1, min_value = 0, max_value = 1000000)
        h = st.number_input('Type the value for the hypotenuse: ', value = 0, step = 1, min_value = 0, max_value = 1000000)
        leg1 = st.number_input('Type the value for one leg: ', value = 0, step = 1, min_value = 0, max_value = 1000000)
        leg2_1 = st.number_input('Type the value for the other leg: ', value = 0, step = 1, min_value = 0, max_value = 1000000)

        if done_left:
            c, cc = leg1, leg2_1
            mp.dps = round(mp.ln(rango_1)/2) 
            #a logarithmic function decreases its growth while the x value goes up, so its useful to assign the number of 
            # decimal values without getting big numbers
            if c>cc: # deciding which var will be the longest leg
                c1, c2 = c, cc
            elif cc > c:
                c1, c2 = cc, c
            elif c == cc:
                c1, c2 = c, cc
            triang = Ptgrs(h, c1, c2) #Ptgrs class var
            resta = mpf(triang.c2/rango_1) #decides how much the tiny leg will be shrinked per loop, ej: 2cm/100Loops = 0.02
            difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
            x = [] #x axis
            c = [] #full of zeros (for comparisons)
            triangs = [] #it gives access to any given triangle (h, c1, c2)
            aux = 0

            bar_1 = st.progress(0, text= "Loading and saving all values...")

            for i in range(rango_1):
                progress = int(( (i+1) / rango_1) * 100)
                bar_1.progress(progress, text= "Loading and saving all values...")
                if triang.h == triang.c1 == triang.c2:
                    triang.c2-resta
                if triang.check(): #if the triangle actually is a right triangle
                    triangs.append({'hptns': triang.h, 'c1': triang.c1, 'c2': triang.c2})
                    triang.c2 -= resta #substracts var
                    difftotal.append(triang.h - triang.c1) #saves the difference to a list
                    x.append(i) #adds consecutive numbers to a list
                    c.append(0.) #adds zeros
                triang.pitagorazo('h')
            scale = 10**resta
            st.write("Done!")

def draw_right_column():
    global status, difftotal, x, c, scale
    with right:
        done_right = False
        if st.button("\n2) Choose the tiny leg's length and it's substraction per loop.", key = 'r', type = 'primary'):
            done_right = True
            status = 'R'
        
        substract = st.number_input('Type the number that will be substracted from the tiny leg: ', value = 0., step = 0.001, min_value = 0., max_value = 1000000.)
        leg2 = st.number_input('Type the value for the tiny leg: ', value = 0, step = 1, min_value = 0, max_value = 1000000)

        if done_right:
            if leg2 < (substract*3):
                st.write("The tiny leg must be at least 3 times bigger than the substraction value.")
            leg2 = mpf(leg2)
            substract = mpf(substract)

            triang = Ptgrs(leg2, leg2, leg2) #Ptgrs class var, 
            #as the program just asked for one leg, let the triangle have two equal legs, same with the hypotenuse
            triang.pitagorazo('h') #to make an actual right triangle
            rango = triang.c2/substract#tiny leg divided by the substract value is the same as the range
            #i used the range for the basic program, as this doesn't use range, i just cleared the equation
            mp.dps = round(mp.ln(rango)/2) 
            difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
            x = [] #x axis
            c = [] #full of zeros (for comparisons)
            triangs = []

            bar_2 = st.progress(0, text= "Loading and saving all values...")

            for i in range(round(rango)):
                progress = int(( (i+1) / rango) * 100)
                bar_2.progress(progress, text= "Loading and saving all values...")
                if triang.h == triang.c1 == triang.c2:
                    triang.c2-substract
                if triang.check(): #if the triangle actually is a right triangle
                    triangs.append({'hptns': triang.h, 'c1': triang.c1, 'c2': triang.c2})
                    triang.c2 -= substract #substracts var
                    difftotal.append(triang.h - triang.c1) #saves the difference to a list
                    x.append(i) #adds consecutive numbers to a list
                    c.append(0.) #adds zeros
                triang.pitagorazo('h')
            scale = 10**substract
            st.write("Done!")

draw_left_column()
draw_right_column()
if status == 'L' or status == 'R':
    return_results(difftotal, x, c, scale)
