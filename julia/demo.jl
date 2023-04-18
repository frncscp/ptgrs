include("Ptgrs.jl")
using Plots
using Printf

function isanumber(n)
    return tryparse(Float64, n) !== nothing
end

function input(question)
    print(question)
    answer = readline()
    return answer
end

function same_line_percentage(i, rango)
    @printf("Loading: %2.f%%", (i/rango)*100)
    print("\e[2K") # clear whole line
    print("\e[1G") # move cursor to column 1
end

while true
    print("$('*'^10)PTGRS$('*'^11)\n****github.com/frncscp****\n$('*'^26)\n\nThis program answers to the following questions:\nWhat is the difference between the hypotenuse and the longest leg of a\nright triangle that is the smallest (empirically possible) to find?\nWhat would the graph look like?\n\nBy looping through a set of right triangles, it will store the difference\nbetween the long leg and the hypotenuse.\n\nChoose you option:\n1)Choose range and triangle sides' length.\n2)Choose the tiny leg's length and it's substraction per loop.\n(Any other option will close the program.)\n(If you get a minimum difference of 0, try to run the program again with a bigger range.)\n\nType here: ")

    choice = convert(String, readline())

    if choice != "1" && choice != "2"
        println("Wrong option")
        break
    else
        println("Option $(choice) has been chosen")
    end

    save_image = input("Press 1 if you want to save the image\nPress anything to continue: ")

    if choice == "1"

        vars = Dict(
            "range" => input("1. Type range: "),
            "hypotenuse" => input("2. Type the value for the hypotenuse: "),
            "leg1" => input("3. Type the value for one leg: "),
            "leg2" => input("4. Type the value for the other leg: "))

        for (key, value) in vars
            while !isanumber(value)
                println("Wrong data type on $key type, $value is not a number.\nTry Again: ")
                new_data = readline()
                value = new_data
            end
        end

        rango = round(parse(Float64, vars["range"]))
        h = parse(Float64, vars["hypotenuse"])
        c = parse(Float64, vars["leg1"])
        cc = parse(Float64, vars["leg2"])

        if c > cc # deciding which var will be the longest leg
            c1, c2 = c, cc
        elseif cc > c
            c1, c2 = cc, c
        elseif c == cc
            c1, c2 = c, cc
        end
        
        triang = Ptgrs(h, c1, c2)

        resta = triang.c2/rango #decides how much the tiny leg will be shrinked per loop, ej: 2cm/100Loops = 0.02
        difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
        x = [i for i in 1:rango-1] #x axis
        c = [0 for i in 1:rango-1] #full of zeros (for comparisons)
        triangs = [] #it gives access to any given triangle (h, c1, c2)

        for i in 1:rango
            same_line_percentage(i, rango)
            
            if triang.h == triang.c1 == triang.c2
                triang.c2 -= resta
            end

            if check(triang)
                push!(triangs, ("hptns" => triang.h, "c1" => triang.c1, "c2" => triang.c2))
                triang.c2 -= resta
                push!(difftotal, triang.h-triang.c1)
            end

            pitagorazo(triang, "h")
        end

        scale = 10 ^ resta  

    elseif choice == "2"

        vars = Dict(
            "substract" => input("Type the number that will be substracted from the tiny leg: "),
            "leg2" => input("Type the value for the tiny leg: "))


        for (key, value) in vars
            while !isanumber(value)
                println("Wrong data type on $key type, $value is not a number.\nTry Again: ")
                new_input = readline()
                value = new_input
            end
        end

        substract = parse(Float64, vars["substract"])
        leg2 = parse(Float64, vars["leg2"])

        while leg2 < substract*3 
            println("Insufficient value for leg length, the minimum value possible is $(3*vars["substract"])\nTry again: ")
            leg2 = readline()
            while !isanumber(leg2)
                println("Wrong data type on $(label) type\nTry Again: ")
            end
        end

        triang = Ptgrs(leg2, leg2, leg2)
        #= as the program just asked for one leg, let the triangle 
            have two equal legs, same with the hypotenuse =#
        pitagorazo(triang, "h")
        rango = round(triang.c2/substract)#tiny leg divided by the substract value is the same as the range
        #i used the range for the basic program, as this doesn't use range, i just cleared the equation
        difftotal = [] #substractions between hypotenuse and the longest leg, it'll be later the y axis on the graph
        x = [] #x axis
        c = [] #full of zeros (for comparisons)
        triangs = []

        for i in 1:round(rango)
            same_line_percentage(i, rango)
            if triang.h == triang.c1 == triang.c2
                triang.c2 -= substract
            end

            if check(triang)
                push!(triangs, ("hptns" => triang.h, "c1" => triang.c1, "c2" => triang.c2))
                triang.c2 -= substract
                push!(difftotal, triang.h-triang.c1)
            end
            pitagorazo(triang, "h")
        end
        scale = 10 ^ substract
    end

    tiniest_diff = difftotal[end]

    for (aux, item) in enumerate(difftotal)
        item*= scale
        difftotal[aux] = item
        aux += 1

    end

    println("The minimum difference between the hypotenuse and the long leg of all right triangles was: $(tiniest_diff).")
    println("Loading plot...\n")
    #the last but one number of the list, before zero, is the minimum difference between the hypotenuse and long leg 

    graf = plot(x, [[0 for i in 1:rango-1], difftotal],
    title = "Limit of difference between the hypotenuse and the long leg of a right triangle with $(rango) iterations.", 
    xlabel = "Iteration", 
    ylabel = "Leg-hypotenuse difference")

    display(graf)

    if save_image == "1"
        filename = input("Type the file's name")
        savefig("$(filename).png")
    end

    println("If you wish to execute a new task, press 1.\nOtherwise, press any key.\nType here: ")
    choice = convert(String, readline())

    if choice == "1"
        continue
    else
        break
    end
end