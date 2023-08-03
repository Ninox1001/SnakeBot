
import time
import os

if os.name == 'nt':
    import msvcrt
    def getch():
        return msvcrt.getch().decode()
else:
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

from dynamixel_sdk import * # Uses Dynamixel SDK library

#********* DYNAMIXEL Model definition *****
MY_DXL = 'X_SERIES'       # 

# Number of neuron
NUMBER_RS_NEURONS = 3


# Control table address

ADDR_TORQUE_ENABLE          = 64
ADDR_GOAL_POSITION          = 116
ADDR_PRESENT_POSITION       = 132
BAUDRATE                    = 57600

# https://emanual.robotis.com/docs/en/dxl/protocol2/
PROTOCOL_VERSION            = 2.0


# Use the actual port assigned to the U2D2.
# ex) Windows: "COM*", Linux: "/dev/ttyUSB*", Mac: "/dev/tty.usbserial-*"
DEVICENAME                  = '/dev/ttyUSB0'
TORQUE_ENABLE               = 1     # Value for enabling the torque
TORQUE_DISABLE              = 0     # Value for disabling the torque
DXL_MOVING_STATUS_THRESHOLD = 20    # Dynamixel moving status threshold


# Initialize PortHandler instance
# Set the port path
# Get methods and members of PortHandlerLinux or PortHandlerWindows
portHandler = PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = PacketHandler(PROTOCOL_VERSION)

# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()


# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()


NUMBER_RS_NEURONS = 3

class RSneuron:
    def __init__(self):
        self.a = 0           # membrane potential
        self.a_old = 0
        self.GoRight = True
        self.ID = 0
rs_neuron = [RSneuron() for _ in range(NUMBER_RS_NEURONS)]

Offset = 1024
time_step = 0.1
angleStep = 120  #10 deg
MaxAngle = 360 #30 deg

i = 0
j = 0

print("begin")

for i in range(NUMBER_RS_NEURONS):
    rs_neuron[i].ID = i + 1
    j = i % 3
    if j == 0:
        rs_neuron[i].a = 240 + Offset
    elif j == 1:
        rs_neuron[i].a = 0 + Offset
    else:
        rs_neuron[i].a = -240 + Offset

# Enable Dynamixel Torque
for i in range(NUMBER_RS_NEURONS):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, rs_neuron[i].ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))
    else:
        print("Dynamixel has been successfully connected")

while 1:
    for i in range(NUMBER_RS_NEURONS):
        rs_neuron[i].a_old = rs_neuron[i].a
        if rs_neuron[i].GoRight:
            rs_neuron[i].a = rs_neuron[i].a_old + angleStep
            if rs_neuron[i].a == MaxAngle + Offset:
                rs_neuron[i].GoRight = False
        else:
            rs_neuron[i].a = rs_neuron[i].a_old - angleStep
            if rs_neuron[i].a == -MaxAngle + Offset:
                rs_neuron[i].GoRight = True

        # Write goal position
        dxl_comm_result, dxl_error = packetHandler.write4ByteTxRx(portHandler, rs_neuron[i].ID, ADDR_GOAL_POSITION, rs_neuron[i].a)
        if dxl_comm_result != COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        elif dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(dxl_error))

    time.sleep(0.1)

    for i in range(NUMBER_RS_NEURONS):
        print(f"Neuron: {rs_neuron[i].ID} = {rs_neuron[i].a}", end="")
        if not rs_neuron[i].GoRight:
            print("   |  <--  ")
        else:
            print("   |  -->  ")

    print("------------------------------")



# Disable Dynamixel Torque
for i in range(NUMBER_RS_NEURONS):
    dxl_comm_result, dxl_error = packetHandler.write1ByteTxRx(portHandler, rs_neuron[i].ID, ADDR_TORQUE_ENABLE, TORQUE_DISABLE)
    if dxl_comm_result != COMM_SUCCESS:
        print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
    elif dxl_error != 0:
        print("%s" % packetHandler.getRxPacketError(dxl_error))

# Close port
portHandler.closePort()
