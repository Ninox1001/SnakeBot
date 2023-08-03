
import time
NUMBER_RS_NEURONS = 3

class RSneuron:
    def __init__(self):
        self.a = 0           # membrane potential
        self.a_old = 0
        self.GoRight = True

rs_neuron = [RSneuron() for _ in range(NUMBER_RS_NEURONS)]

time_step = 0.1
angleStep = 10
MaxAngle = 30

i = 0
j = 0

def setup():
    print("begin")

    for i in range(NUMBER_RS_NEURONS):
        j = i % 3
        if j == 0:
            rs_neuron[i].a = 20
        elif j == 1:
            rs_neuron[i].a = 0
        else:
            rs_neuron[i].a = -20

def loop():
    # CPG_______________________________________________________________

    for i in range(NUMBER_RS_NEURONS):
        rs_neuron[i].a_old = rs_neuron[i].a
        if rs_neuron[i].GoRight:
            rs_neuron[i].a = rs_neuron[i].a_old + 10
            if rs_neuron[i].a == MaxAngle:
                rs_neuron[i].GoRight = False
        else:
            rs_neuron[i].a = rs_neuron[i].a_old - 10
            if rs_neuron[i].a == -MaxAngle:
                rs_neuron[i].GoRight = True

    time.sleep(1)

    for i in range(NUMBER_RS_NEURONS):
        print(f"Neuron: {i} = {rs_neuron[i].a}", end="")
        if not rs_neuron[i].GoRight:
            print("   |  <--  ")
        else:
            print("   |  -->  ")

    print("------------------------------")

# Appel des fonctions setup() et loop()
setup()
while True:
    loop()
