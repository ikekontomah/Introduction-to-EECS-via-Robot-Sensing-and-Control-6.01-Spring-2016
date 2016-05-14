from lib601.poly import Polynomial


class System:

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator

    def calculate_step(self, state, inp):
        return (state, inp)

    def simulator(self):
        return SystemSimulator(self)

    def poles(self):
        
        x=[]
        for i in range(self.denominator.order+1):
        
            u=self.denominator.coeff(i)
            x.append(u)
        
        x.reverse()
    
        pol = Polynomial(x)
        u=pol.roots()
        if self.denominator.order>=self.numerator.order:
            return u
        else:
            return u+ [0]*(self.numerator.order-self.denominator.order)

            

    def dominant_pole(self):
        max_pole=0
        
        for i in (self.poles()):
            if abs(i)>abs(max_pole):
                max_pole=i
        return max_pole
            


class SystemSimulator:

    def __init__(self, system):
        self.system = system
        self.reset()

    def step(self, inp):
        (new_state, out) = self.system.calculate_step(self.state, inp)
        self.state = new_state
        return out

    def reset(self):
        self.state = self.system.initial_state

    def get_response(self, inputs, reset=True):
        if reset:
            self.reset()
        return [self.step(inp) for inp in inputs]


class R(System):

    def __init__(self, Output0=0):

        self.numerator = Polynomial([0, 1])
        self.denominator = Polynomial([1])
        self.initial_state = Output0

    def calculate_step(self, state, inp):
        output = state
        new_state = inp

    

    

        return (new_state, output)


class Gain(System):

    def __init__(self, k):
        self.k = k
        self.initial_state = None  # modify if necessary
        self.numerator = Polynomial([k])
        self.denominator = Polynomial([1])

    def calculate_step(self, state, inp):
        self.state = state
        self.inp = inp
        new_state = self.inp
        output = self.k * self.state
        return (new_state, output)


class FeedforwardAdd(System):

    def __init__(self, s1, s2):
        self.s1 = s1
        self.s2 = s2
        self.initial_state = (s1.initial_state, s2.initial_state)
        n_1 = s1.numerator
        n_2 = s2.numerator
        d_1 = s1.denominator
        d_2 = s2.denominator

        self.numerator = n_1 * d_2 + n_2 * d_1
        self.denominator = d_1 * d_2

    def calculate_step(self, state, inp):
        (s1_state, s2_state) = state
        (new_state_s1, out1) = self.s1.calculate_step(s1_state, inp)
        (new_state_s2, out2) = self.s2.calculate_step(s2_state, inp)
        new_state = (new_state_s1, new_state_s2)
        output = out1 + out2

        return (new_state, output)


class Cascade(System):

    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2
        n_1 = s1.numerator
        n_2 = s2.numerator
        d_1 = s1.denominator
        d_2 = s2.denominator
        self.numerator = n_1 * n_2
        self.denominator = d_1 * d_2

    def calculate_step(self, state, inp):
        (s1_state, s2_state) = state
        new_s1_state = self.s1.calculate_step(s1_state, inp)[0]
        a = self.s1.calculate_step(s1_state, inp)[1]
        new_s2_state = self.s2.calculate_step(s2_state, a)[0]
        output = self.s2.calculate_step(new_s2_state, a)[1]
        new_state = (new_s1_state, new_s2_state)
        return (new_state, output)


class FeedbackAdd(System):

    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state, s2.initial_state)
        self.s1 = s1
        self.s2 = s2
        n_1 = s1.numerator
        n_2 = s2.numerator
        d_1 = s1.denominator
        d_2 = s2.denominator

        self.numerator = n_1 * d_2
        self.denominator = d_1 * d_2 - n_1 * n_2

    def calculate_step(self, state, inp):
        (s1_state, s2_state) = state


a=R()
print(a.numerator,a.denominator)
b=Cascade(R(0),R(0))
print(b.numerator,"expect R**2",b.denominator,"expect 1")
c=FeedforwardAdd(R(0),R(0))
print(c.numerator,"expect 2*R", c.denominator ,"expect 1")
d=FeedbackAdd(R(0),R(0))
print(d.numerator,"expect R" , d.denominator , "expect 1 - R**2")


y=System(Polynomial([0,1]),Polynomial([1,-1,-1]))
print(y.poles())

