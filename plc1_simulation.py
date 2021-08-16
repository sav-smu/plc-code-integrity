import csv
import numpy as np

from plc import plc1,plc2,plc3,plc4,plc5,plc6
import sys,os
sys.path.insert(0,os.getcwd())
from io_plc.IO_PLC import DI_WIFI
from SCADA import H
from IO import *


from PLC_simulation import plc_simulation




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

p = {"LIT101_AL": 500, "LIT101_AH": 800, "LIT301_AL": 800, "LIT301_AH": 1000, "LIT401_AL": 800, "LIT401_AH": 1000,
     "LIT601_AL": 500, "LIT601_AH": 800, "LIT602_AL": 500, "LIT602_AH": 800, "LIT101_ALL": 250, "LIT101_AHH": 1200,
     "LIT301_ALL": 250, "LIT301_AHH": 1200, "LIT401_ALL": 250, "LIT401_AHH": 1200}
Sec_P=0
Min_P=0
i=0
input=[]
output=[]
# plc_simulation.test_plc1_input(HMI)
while (i<100000):
     a = plc_simulation.generate_plc1_input(HMI,p)
     input.append(a)
     plc_simulation.assumption(HMI)
     # plc_simulation.test_plc1_input(HMI)
     # plc_simulation.DI_generation_test(IO_P1,IO_P2,IO_P3,IO_P4,IO_P5,IO_P6)
     PLC1.Pre_Main_Raw_Water(IO_DI_WIFI, IO_P1, HMI, Sec_P, Min_P)
     b=plc_simulation.print_plc1_output(IO_P1)
     output.append(b)
     i=i+1

input__path="data/plc1_input.npy"
output__path="data/plc1_output.npy"
input=np.array(input)
output=np.array(output)
input.dump(input__path)
output.dump(output__path)
print (input)
print (output)
