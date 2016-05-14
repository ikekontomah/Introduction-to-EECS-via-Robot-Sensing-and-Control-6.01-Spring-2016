def make_system_model(K):
    x=Cascade(Gain(K),FeedbackAdd(R(0),Gain(1)))
    y=Cascade(Gain(-1),R(0))
    return FeedbackAdd(x,y)
def minimum_linear(f, x0, x1, threshold):
    
    x = float(x0)
    bestX = x
    bestFX = f(x)
    while x < x1:
        test = f(x)
        if test < bestFX:
            bestFX = test
            bestX = x
        x += threshold
    return (bestX, bestFX)
def minimum_bisection(f, x0, x1, threshold=1e-4, h=1e-6):
    
    f_prime = lambda x: (f(x+h)-f(x-h))/(2.0*h) # approximate derivative
    right = (x1,f_prime(x1))
    left = (x0,f_prime(x0))
    while abs(right[0] - left[0]) > threshold:
        new_x = ((right[0]+left[0])/2.)
        new_d = f_prime(new_x)
        if (new_d < 0 and left[1] < 0) or (new_d > 0 and left[1] > 0):
            left = (new_x,new_d)
        else:
            right = (new_x,new_d)
    return left[0],f(left[0])
