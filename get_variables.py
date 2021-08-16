from plc_offline import plc1,plc2,plc3,plc4,plc5,plc6
from variables_initialization import generate_variables
import sys,os
sys.path.insert(0,os.getcwd())
from SCADA import H
from IO import *
from data_process.get_OTdata import get_input
from PLC_simulation import plc_simulation
import time
import pandas as pd
# Initiating Plant
# Defining I/O
IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()
print ("Initializing SCADA HMI")
HMI = H()
print ("Initializing PLCs\n")


# HMI.LIT101.Pv=1100
# HMI.LIT101.set_alarm()
# print (HMI.LIT101.AL)
# generate_variables.generate_plc_input(HMI)
PLC1 = plc1.plc1(HMI)
PLC2 = plc2.plc2(HMI)
PLC3 = plc3.plc3(HMI)
PLC4 = plc4.plc4(HMI)
# PLC5 = plc5.plc5(HMI)
PLC6 = plc6.plc6(HMI)
# print ("Now starting Simulation")
# # Main Loop Body

# input_path=os.getcwd()+"/data/CISS2020-OL.July27_Attestor.xlsx"
# print(input_path)
# df=pd.read_excel(input_path)
# get_input(df,HMI,0)
