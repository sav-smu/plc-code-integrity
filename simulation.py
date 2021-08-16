from plc import plc1,plc2,plc3,plc4,plc5,plc6
file_abs = "E:\python_file\plc1_6.txt"
import sys,os
sys.path.insert(0,os.getcwd())
from io_plc.IO_PLC import DI_WIFI
from SCADA import H
from IO import *
from plant_ode.plant_ode import plant
from PLC_simulation import plc_simulation
# maxstep = 200*60*30#*60#*2 # time is counted in 0.005 seconds, 200*x*y, x unit seconds, y unit minutes
maxstep = 200*60*30#*60#*2 # time is counted in 0.005 seconds, 200*x*y, x unit seconds, y unit minutes
# Initiating Plant
Plant = plant(maxstep)
# Defining I/O
IO_DI_WIFI = DI_WIFI()
IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()
print ("Initializing SCADA HMI")
HMI = H()
print ("Initializing PLCs\n")
PLC1 = plc1.plc1(HMI)
PLC2 = plc2.plc2(HMI)
PLC3 = plc3.plc3(HMI)
PLC4 = plc4.plc4(HMI)
PLC5 = plc5.plc5(HMI)
PLC6 = plc6.plc6(HMI)
print ("Now starting Simulation")
# Main Loop Body
for time in range(maxstep):
#Second, Minute and Hour pulse
    Sec_P = not bool(time%(200))
    Min_P = not bool(time%(200*60))
#solving out plant odes in 5 ms
    Plant.Actuator(IO_P1,IO_P2,IO_P3,IO_P4,IO_P5,IO_P6)
    Plant.Plant(IO_P1,IO_P2,IO_P3,IO_P4,IO_P5,IO_P6,time)
# initialize
    p={"LIT101_AL":500,"LIT101_AH":800,"LIT301_AL":800,"LIT301_AH":1000,"LIT401_AL":800,"LIT401_AH":1000,"LIT601_AL":500,"LIT601_AH":800,"LIT602_AL":500,"LIT602_AH":800,"LIT101_ALL":250,"LIT101_AHH":1200,"LIT301_ALL":250,"LIT301_AHH":1200,"LIT401_ALL":250,"LIT401_AHH":1200}
    HMI.LIT101.AH = Plant.result[time][2] > p["LIT101_AH"]
    HMI.LIT101.AL = Plant.result[time][2] < p["LIT101_AL"]
    # print "point1"
    # print HMI.LIT101.AL
    HMI.LIT301.AH = Plant.result[time][3] > p["LIT301_AH"]
    HMI.LIT301.AL = Plant.result[time][3] < p["LIT301_AL"]
    HMI.LIT401.AH = Plant.result[time][4] > p["LIT401_AH"]
    HMI.LIT401.AL = Plant.result[time][4] < p["LIT401_AL"]
    HMI.LIT101.AHH = Plant.result[time][2] > p["LIT101_AHH"]

    HMI.LIT101.ALL = Plant.result[time][2] < p["LIT101_ALL"]
    HMI.LIT301.AHH = Plant.result[time][3] > p["LIT301_AHH"]
    HMI.LIT301.ALL = Plant.result[time][3] < p["LIT301_ALL"]
    HMI.LIT401.AHH = Plant.result[time][4] > p["LIT401_AHH"]
    HMI.LIT401.ALL = Plant.result[time][4] < p["LIT401_ALL"]

#PLC working
    plc_simulation.print_plc1_input(HMI,Plant.result[time][2],Plant.result[time][3],p)
    PLC1.Pre_Main_Raw_Water(IO_DI_WIFI,IO_P1,HMI,Sec_P,Min_P)
    plc_simulation.print_plc1_output(IO_P1)
    print Plant.result[time][2]
    print Plant.result[time][3]
    PLC2.Pre_Main_UF_Feed_Dosing(IO_DI_WIFI,IO_P2,HMI,Sec_P,Min_P)
    PLC3.Pre_Main_UF_Feed(IO_DI_WIFI,IO_P3,HMI,Sec_P,Min_P)
    PLC4.Pre_Main_RO_Feed_Dosing(IO_DI_WIFI,IO_P4,HMI,Sec_P,Min_P)
    PLC5.Pre_Main_High_Pressure_RO(IO_DI_WIFI,IO_P5,HMI,Sec_P,Min_P)
    PLC6.Pre_Main_Product(IO_DI_WIFI,IO_P6,HMI,Sec_P,Min_P)
    # print (Plant.result[time])
    # print ('{0}\n'.format(Plant.result[time][2:]))
    # print Plant.result[time][2]
    # print p["LIT101_AL"]
    # print "point2"
    # print HMI.LIT101.AL
# HMI.LIT301.AL = Plant.result[time][3] < p["LIT301_AL"]
# HMI.LIT401.AH = Plant.result[time][4] > p["LIT401_AH"]
# HMI.LIT401.AL = Plant.result[time][4] < p["LIT401_AL"]
# HMI.LIT101.AHH = Plant.result[time][2] > p["LIT101_AHH"]
# HMI.LIT101.ALL = Plant.result[time][2] < p["LIT101_ALL"]
# HMI.LIT301.AHH = Plant.result[time][3] > p["LIT301_AHH"]
# HMI.LIT301.ALL = Plant.result[time][3] < p["LIT301_ALL"]
# HMI.LIT401.AHH = Plant.result[time][4] > p["LIT401_AHH"]
# HMI.LIT401.ALL = Plant.result[time][4] < p["LIT401_ALL"]
    # with open(file_abs, 'a') as f:
    #     f.write('{0}\n'.format(Plant.result[time][2:]))
    # print maxstep
#print IO_P3.P301.DI_Run or IO_P3.P302.DI_Run and IO_P3.MV301.DI_ZSC and IO_P3.MV302.DI_ZSO and IO_P3.MV303.DI_ZSC and IO_P3.MV304.DI_ZSC and IO_P6.P602.DI_Run
#print HMI.Cy_P3.UF_FILTRATION_MIN