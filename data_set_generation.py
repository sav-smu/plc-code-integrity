from plc_offline import plc1,plc2,plc3,plc4,plc6
import sys,os
sys.path.insert(0,os.getcwd())
from SCADA import H
from IO import *
from PLC_simulation import plc_simulation
import time
import pandas as pd
from variables_initialization.generate_variables import generate_plc_input
from variables_initialization.generate_variables import get_all_input
import numpy as np
def data_set_generation(input_path,output_path,length):
    input = []
    output = []
    IO_P1 = P1()
    IO_P2 = P2()
    IO_P3 = P3()
    IO_P4 = P4()
    IO_P5 = P5()
    IO_P6 = P6()
    index = 0
    while (index < length):
        HMI = H()
        generate_plc_input(HMI)
        a=get_all_input(HMI)
        print (len(a))
        input.append(a)
        # print(get_all_input(HMI))
        PLC1 = plc1.plc1(HMI)
        PLC2 = plc2.plc2(HMI)
        PLC3 = plc3.plc3(HMI)
        PLC4 = plc4.plc4(HMI)
        PLC6 = plc6.plc6(HMI)
        PLC1.Pre_Main_Raw_Water(IO_P1, HMI)
        PLC2.Pre_Main_UF_Feed_Dosing(IO_P2, HMI)
        PLC3.Pre_Main_UF_Feed(IO_P3, HMI)
        PLC4.Pre_Main_RO_Feed_Dosing(IO_P4, HMI)
        PLC6.Pre_Main_Product(IO_P6, HMI)
        DO_all = plc_simulation.print_all_output(IO_P1, IO_P2, IO_P3, IO_P4, IO_P5, IO_P6)
        b=DO_all
        output.append(b)
        # future_state1 = DO_all[0]
        # future_state2 = DO_all[1]
        # future_state3 = DO_all[2]
        # future_state4 = DO_all[3]
        # future_state6 = DO_all[5]
        # print(DO_all)
        index = index + 1

    input = np.array(input)
    output = np.array(output)
    input.dump(input_path)
    output.dump(output_path)
    print(input)
    print(output)


    # print (DO_all)
#
# print (input_path)


if __name__ == "__main__":
    length=1
    input_path = "data/plc_input_length"+str(length)+".npy"
    output_path ="data/plc_output_length"+str(length)+".npy"
    data_set_generation(input_path,output_path,length)