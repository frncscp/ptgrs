mutable struct Ptgrs
    h::Float64
    c1::Float64
    c2::Float64
end

function check(self::Ptgrs, epsilon = .005) #saber si se cumple el teorema de pitágoras
    return self.h%((self.c1^2)+(self.c2^2))^.5 < epsilon
end

function pitagorazo(self::Ptgrs, lado::String)
    if lado == "h"
        self.h = (self.c1^2 + self.c2^2)^.5
        return self.h
    elseif lado == "c1"
        self.c1 = (self.h^2 + self.c2^2)^.5
        return self.c1
    elseif lado == "c2"
        self.c2 = (self.h^2 + self.c1^2)^.5
        return self.c2
    else
        return -1
    end
end