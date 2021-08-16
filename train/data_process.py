import numpy as np
import pandas as pd
import os
import math
from sklearn.naive_bayes import BernoulliNB
def code_output(output):
    if np.size(output)>0:
        l=len(output)
        s=len(output[0])
    else:
        print ("Input cannot be null!")
    new_output=[]
    for i in range(l):
        t=0
        for j in range(s):
           t=output[i][j]*math.pow(2,j)+t
        new_output.append(t)
    return new_output

# def data_process(input_path,output_path):
#     input = np.load(input_path, allow_pickle=True)
#     output = np.load(output_path, allow_pickle=True)
#     new_output = code_output(output)
#     return input,new_output

def single_actuator_set(output_path,plc_ind,actuator_ind):
    output = np.load(output_path, allow_pickle=True)
    length=len(output)
    new_set=[]
    for i in range(length):
        new_set.append(output[i][plc_ind][actuator_ind])

    return new_set

def single_plc_set(output_path,plc_ind):
    output = np.load(output_path, allow_pickle=True)
    length = len(output)
    new_set = []
    l = len(output[0][plc_ind])
    for i in range(length):
        t=0
        print (output[i][plc_ind])
        for j in range(l):
           t=output[i][plc_ind][j]*math.pow(2,j)+t
        new_set.append(t)

    return new_set



if __name__ == '__main__':
    output_path = os.path.abspath('..') + "/data/plc_output.npy"
    new_set=single_plc_set(output_path,3)
    print (new_set)


    # plc1_output_vector = [P1.MV101.DO_Open, P1.MV101.DO_Close, P1.P101.DO_Start, P1.P102.DO_Start]
    # plc2_output_vector= [P2.MV201.DO_Open, P2.MV201.DO_Close, P2.P201.DO_Start, P2.P202.DO_Start, P2.P203.DO_Start, P2.P204.DO_Start, P2.P205.DO_Start, P2.P206.DO_Start]
    # plc3_output_vector = [P3.MV301.DO_Open, P3.MV301.DO_Close,P3.MV302.DO_Open, P3.MV302.DO_Close,P3.MV303.DO_Open, P3.MV303.DO_Close,P3.MV304.DO_Open, P3.MV304.DO_Close, P3.P301.DO_Start, P3.P302.DO_Start]
    # plc4_output_vector = [P4.P401.DO_Start,P4.P402.DO_Start,P4.P403.DO_Start,P4.P404.DO_Start,P4.UV401.DO_Start]
    # plc5_output_vector = [P5.MV501.DO_Open,P5.MV501.DO_Close,P5.MV502.DO_Open,P5.MV502.DO_Close,P5.MV503.DO_Open,P5.MV503.DO_Close,P5.MV504.DO_Open,P5.MV504.DO_Close]
    # plc6_output_vector = [P6.P601.DO_Start,P6.P602.DO_Start]
    #output[index][indexofPLC][indexofactuiator]