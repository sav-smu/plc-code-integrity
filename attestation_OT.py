from plc_offline import plc1,plc2,plc3,plc4,plc5,plc6
import sys,os
sys.path.insert(0,os.getcwd())
from SCADA import H
from IO import *
from PLC_simulation import plc_simulation
import time
import pandas as pd
from data_process.get_OTdata import get_OTinput
from attestation import checker_offline



input_path=os.getcwd()+"/data/August06_Attestor.csv"
# input_path=os.getcwd()+"/data/July30_Attestor.csv"
df=pd.read_csv(input_path)

IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()
index=0
plc1_delay=[0,0]
plc2_delay=[0,0,0,0]
plc3_delay=[0,0,0,0,0]
plc4_delay=[0,0,0]
TP=[]
# mv101_delay=0
# p101_delay=0
# mv201_delay=0
# p201_delay=0
# p203_delay=0
# p205_delay=0
# mv301_delay=0
# mv302_delay=0
# mv303_delay=0
# mv304_delay=0
# p301_delay=0
# p401_delay=0
# p403_delay=0
# uv401_delay=0
while (index<20000):

    HMI = H()
    get_OTinput(df,HMI,index)
    # print ("P201")
    # print (HMI.P201.Status)
    # print ("AIT201")
    # print (HMI.AIT201.AL)
    # print (HMI.AIT201.Pv)
    # print ("FIT201")
    # print (HMI.FIT201.Pv)
    #
    # print (HMI.FIT201.AH)
    # print ("Initializing PLCs\n")
    PLC1 = plc1.plc1(HMI)
    PLC2 = plc2.plc2(HMI)
    PLC3 = plc3.plc3(HMI)
    PLC4 = plc4.plc4(HMI)
    PLC5 = plc5.plc5(HMI)
    PLC6 = plc6.plc6(HMI)

    PLC1.Pre_Main_Raw_Water(IO_P1, HMI)
    PLC2.Pre_Main_UF_Feed_Dosing(IO_P2, HMI)
    PLC3.Pre_Main_UF_Feed(IO_P3, HMI)
    PLC4.Pre_Main_RO_Feed_Dosing(IO_P4, HMI)
    PLC5.Pre_Main_High_Pressure_RO(IO_P5,HMI)
    PLC6.Pre_Main_Product( IO_P6, HMI)
    DO_all = plc_simulation.print_all_output(IO_P1, IO_P2, IO_P3, IO_P4, IO_P5, IO_P6)
    future_state1 = DO_all[0]
    future_state2 = DO_all[1]
    future_state3 = DO_all[2]
    future_state4 = DO_all[3]
    future_state5 = DO_all[4]
    future_state6=DO_all[5]
    get_OTinput(df,HMI,index+1)
    if not checker_offline.plc1_check_offline(future_state1, HMI,plc1_delay):
        TP.append(index)
        print (index)
        print (DO_all)
    if not checker_offline.plc2_check_offline(future_state2, HMI,plc2_delay):
        TP.append(index)
        print (index)
        print (DO_all)
    if not checker_offline.plc3_check_offline(future_state3,HMI,plc3_delay):
        TP.append(index)
        print (index)
        print (DO_all)
    if not checker_offline.plc4_check_offline(future_state4, HMI,plc4_delay):
        TP.append(index)
        print (index)
        print (DO_all)
    # if not checker_offline.plc5_check_offline(future_state5, HMI):
    #     print (index)
    #     print (DO_all)



    index=index+1

print (TP)
    # print (DO_all)
#
# print (input_path)
