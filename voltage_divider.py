from soar.io import io
from lib601.plotWindow import PlotWindow

######################################################################
###
###          Brain methods
###
######################################################################


def on_load():
    pass

def on_start():
    global bread_crumbs
    bread_crumbs=False
    robot.positions = []

global memory
memory = []

def on_step():
    v_neck,v_left,v_right,_ = io.get_analog_inputs()
    print('Neck:',v_neck,'Left:',v_left,'Right:',v_right)

    k_r=2
    aV = v_left/2 + v_right/2
    k_f = -0.5

    global memory
   
   
    if (v_right < 0.48 or v_left < 0.48) and len(memory) == 0:        
        io.set_forward(0)
        io.set_rotational(0)

    elif (v_right < 0.48 or v_left < 0.48) and len(memory) != 0:
        aV = memory[0][0]
        v_neck = memory[0][1]
        io.set_forward(-k_f*(aV - 2.0))
        io.set_rotational(-k_r*(v_neck-3.5))

        memory.pop(0)

    else:
        memory.insert(0,(aV,v_neck))
        io.set_forward(k_f*(aV - 2.0))
        io.set_rotational(k_r*(v_neck-3.5))
       

    if bread_crumbs:
        robot.positions.append(io.get_position()[:-1])

def on_stop():
    if bread_crumbs:
        PlotWindow(title="Robot Position").scatter(*list(zip(*robot.positions)))

def on_shutdown():
    pass