class R(System):
    def __init__(self, output0=0):
        self.initial_state = output0# modify if necessary

    def calculate_step(self, state, inp):
        output=state
        new_state=inp
        
        return (new_state,output)

class Gain(System):
    def __init__(self, k):
        self.initial_state = 0
        self.k=k# modify if necessary

class FeedforwardAdd(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state,s2.initial_state)
        self.s1=s1
        self.s2=s2

    def calculate_step(self, state, inp):
        s1_state,s2_state=state
        new_state_1,out_1=self.s1.calculate_step(s1_state,inp)
        new_state_2,out_2=self.s2.calculate_step(s2_state,inp)
        new_state=(new_state_1,new_state_2)
        output=out_1 + out_2
        
        return (new_state, output)

class Cascade(System):
    def __init__(self, s1, s2):
        self.initial_state = (s1.initial_state,s2.initial_state)
        self.s1=s1
        self.s2=s2

    def calculate_step(self, state, inp):
        s1_state,s2_state=state
        new_state_s1=self.s1.calculate_step(s1_state,inp)[0]
        a=self.s1.calculate_step(s1_state,inp)[1]
        new_state_s2=self.s2.calculate_step(s2_state,a)[0]
        output=self.s2.calculate_step(s2_state,a)[1]
        new_state=(new_state_s1,new_state_s2)
        
        return (new_state, output)

AveragingFilter2 = Cascade(Gain(0.5),FeedforwardAdd(Gain(1),R(0)))

def delay_n(n):
    if n == 0:
        return Gain(1)
    else:
        return Cascade(delay_n(n-1),R(0))

def averaging_filter(k):
    a=Gain(1/k)
    for n in range(1,k):
        a=FeedforwardAdd(a,Cascade(Gain(1/k),delay_n(n)))
    return a

import math
class Polynomial:
    # initialize the Polynomial with a list of coefficients
    # the coefficient list starts with the lowest-order term
    
    def __init__(self, c):
        self.c = c
        self.rorder = self.c[::-1]
        count = 0
        for ele in self.rorder:
            if ele == 0:
                count+=1
                
            else:
                break
                
                
            
        self.order = len(self.c)-1-count

    # return the coefficient associated with the x**i term
    def coeff(self,i):
        if i in range(0,len(self.c)):
         return self.c[i]
        else:
            return 0

    # return the value of this Polynomial evaluated at x=v
    def val(self, v):
        ans = 0
        for i in range(len(self.c)):
            ans += self.coeff(i)*(v**i)
        return ans

    # add two Polynomials, return a new Polynomial
    def add(self, other):
        ans = [0]*min(len(self.c),len(other.c))
        for i in range(min(len(self.c),len(other.c))):
            ans[i] = self.c[i]+other.c[i]
        if len(self.c)>len(other.c):
            ans.extend(self.c[len(other.c):])
        else:
            ans.extend(other.c[len(self.c):])
        for ele in ans:
            ele = float(ele)
        return Polynomial(ans)
        
            
         
            
    

    # multiply two Polynomials, return a new Polynomial
    def mul(self, other):
        guess = Polynomial([0])
        count = 0
        
        for i in self.c:
            step = [i*element for element in other.c]
            index = count
            count+=1
            
            for e in range(index):
                step.insert(0,0)
            #print(step)
            guess=guess.add(Polynomial(step))
            #print (guess)
        for ele in guess.c:
            ele = float(ele)
            
        return guess
            
            
        

    # return the roots of this Polynomial
    def roots(self):
        
        if (self.order != 1 or self.order!=2)==False:
            
             raise ValueError
        else:
           
            if self.order == 1:
                a = self.c[0]
                b = self.c[1]
                return (-b/a)
                
            else:
                a = self.c[2]
                b = self.c[1]
                c = self.c[0]
                step = b**2-(4*a*c)
                
                if step<0:
                    step = complex(0,math.sqrt(-step))
                else:
                    step = complex(math.sqrt(step),0)
                
                ans1 = (-b+step)/(2*a)
                
                ans2 = (-b-step)/(2*a)
                roots = [ans1,ans2]
                return roots
                
        
            
            

    def __add__(self, other):
        return self.add(other)

    def __mul__(self, other):
        return self.mul(other)

    def __repr__(self):
        return 'Polynomial([%s])' % ', '.join(repr(i) for i in self.coeffs)

    def __str__(self):
        out = ''
        for i in range(self.order,-1,-1):
            c = self.coeff(i)
            if c == 0:
                continue
            if c.real >= 0 and len(out) != 0:
                out += ' + '
            elif len(out) != 0:
                out += ' - '
                c = -c
            if c != 1:
                out += '(%r)' % c
            elif c == 1 and i == 0:
                out += repr(c)
            if i == 1:
                out += 'x'
            elif i != 0:
                out += '(x^%d)' % i
        return out


### Test Cases:

# Test Case 1 (Should print: [2, 0, 100])
# Test of order attribute
import random
p1 = Polynomial([1, 3, 2])
p2 = Polynomial([1])
p3 = Polynomial([random.randint(1, 100) for i in range(101)])
ans = [p1.order, p2.order, p3.order]
print("Test Case 1:", ans)
print("Expected:", [2, 0, 100])

# Test Case 2 (Should print: [4.0, 5.0, 8.0, 6.0, 7.0])
# Test of coeff method
a = Polynomial([4, 5, 8, 6, 7])
ans = [a.coeff(i) for i in range(a.order+1)]
print("Test Case 2:", ans)
print("Expected:", [4.0, 5.0, 8.0, 6.0, 7.0])

# Test Case 3 (Should print: [[10.0, 10.0, 8.0, 4.0], [10.0, 10.0, 8.0, 4.0]])
# Test of add method
p1 = Polynomial([1, 3, 2, 4])
p2 = Polynomial([9, 7, 6])
a = p1.add(p2)
b = p2.add(p1)
ans = [[a.coeff(i) for i in range(a.order+1)], [b.coeff(j) for j in range(b.order+1)]]
print("Test Case 3:", ans)
print("Expected:", [[10.0, 10.0, 8.0, 4.0], [10.0, 10.0, 8.0, 4.0]])

# Test Case 4 (Should print: [2.0, 4.0, 6.0, 1.0, 2.0, 3.0])
# Test of mul method
p1 = Polynomial([1,2,3])
p2 = Polynomial([2, 0, 0, 1])
a = p1.mul(p2)
ans = [a.coeff(i) for i in range(a.order+1)]
print("Test Case 4:", ans)
print("Expected:", [2.0, 4.0, 6.0, 1.0, 2.0, 3.0])

# Test Case 5 (Should print: [(-0.5+0j), (-1+0j)])
# Roots
p = Polynomial([1, 3, 2])
ans = p.roots()
print("Test Case 5:", ans)
print("Expected:", [(-0.5+0j), (-1+0j)])

# Test Case 6 (Should print: [(-0.33333333333333326+0.9428090415820635j), (-0.3333333333333334-0.9428090415820635j)])
# Roots
p = Polynomial([3, 2, 3])
ans = p.roots()
print("Test Case 6:", ans)
print("Expected:", [(-0.33333333333333326+0.9428090415820635j), (-0.3333333333333334-0.9428090415820635j)])


