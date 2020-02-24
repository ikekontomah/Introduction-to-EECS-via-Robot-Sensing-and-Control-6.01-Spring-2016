from lib601.plotWindow import PlotWindow
from lib601.lti import *

def make_controller_model(k):
    return Gain(k)

def make_plant1_model():
    return Cascade(R(0),R(0))
    

def make_plant2_model(initial_sonar, delta_t):
    
    a=Cascade(R(0),Gain(delta_t))
    b=FeedbackAdd(Gain(1),R(-initial_sonar))
    c=Cascade(a,b)
    return c

def make_plant3_model():
    return Gain(-1)

def make_wall_finder_model(k, initial_sonar, delta_t):
    a=Cascade(make_plant1_model(),make_plant2_model(initial_sonar,delta_t))
    b=Cascade(a,make_plant3_model())
    c=Cascade(make_controller_model(k),b)
    return FeedbackAdd(c,Gain(-1))

def estimate_velocities(positions, delta_t):
    
    vel=[]
    for p in range (1,len(positions)) : 
        k=(positions[p]-positions[p-1])/delta_t
        vel.append(k)
    return vel

m=make_wall_finder_model(-0.5,0.8,0.1)
sim = m.simulator()
response = sim.get_response([.5]*200)
PlotWindow().plot(response)
