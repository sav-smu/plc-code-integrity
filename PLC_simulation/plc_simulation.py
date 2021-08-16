from SCADA import H
import random
from device.device import *
import types
def input_generation(P1,P2,P3,P4,P5,P6):
    P1.MV101.DI_ZSO = P1.MV101.DO_Open
    P1.MV101.DI_ZSC = P1.MV101.DO_Close
    P2.MV201.DI_ZSO = P2.MV201.DO_Open
    P2.MV201.DI_ZSC = P2.MV201.DO_Close
    P3.MV301.DI_ZSO = P3.MV301.DO_Open
    P3.MV301.DI_ZSC = P3.MV301.DO_Close
    P3.MV302.DI_ZSO = P3.MV302.DO_Open
    P3.MV302.DI_ZSC = P3.MV302.DO_Close
    P3.MV303.DI_ZSO = P3.MV303.DO_Open
    P3.MV303.DI_ZSC = P3.MV303.DO_Close
    P3.MV304.DI_ZSO = P3.MV304.DO_Open
    P3.MV304.DI_ZSC = P3.MV304.DO_Close
    P5.MV501.DI_ZSO = P5.MV501.DO_Open
    P5.MV501.DI_ZSC = P5.MV501.DO_Close
    P5.MV502.DI_ZSO = P5.MV502.DO_Open
    P5.MV502.DI_ZSC = P5.MV502.DO_Close
    P5.MV503.DI_ZSO = P5.MV503.DO_Open
    P5.MV503.DI_ZSC = P5.MV503.DO_Close
    P5.MV504.DI_ZSO = P5.MV504.DO_Open
    P5.MV504.DI_ZSC = P5.MV504.DO_Close

    P1.P101.DI_Run = P1.P101.DO_Start
    P1.P102.DI_Run = P1.P102.DO_Start
    P3.P301.DI_Run = P3.P301.DO_Start
    P3.P302.DI_Run = P3.P302.DO_Start
    P4.P401.DI_Run = P4.P401.DO_Start
    P4.P402.DI_Run = P4.P402.DO_Start
    P5.P501.DI_Run = P5.P501_VSD_Out.Start or not P5.P501_VSD_Out.Stop
    P5.P502.DI_Run = P5.P502_VSD_Out.Start or not P5.P502_VSD_Out.Stop
    P6.P601.DI_Run = P6.P601.DO_Start
    P6.P602.DI_Run = P6.P602.DO_Start


def DI_generation_test(P1,P2,P3,P4,P5,P6):
    input=[0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, True, True, 0, 0]
    P1.MV101.DI_ZSO = input[0]
    P1.MV101.DI_ZSC = input[1]
    P2.MV201.DI_ZSO = input[2]
    P2.MV201.DI_ZSC = input[3]
    P3.MV301.DI_ZSO = input[4]
    P3.MV301.DI_ZSC = input[5]
    P3.MV302.DI_ZSO = input[6]
    P3.MV302.DI_ZSC = input[7]
    P3.MV303.DI_ZSO = input[8]
    P3.MV303.DI_ZSC = input[9]
    P3.MV304.DI_ZSO = input[10]
    P3.MV304.DI_ZSC = input[11]
    P5.MV501.DI_ZSO = input[12]
    P5.MV501.DI_ZSC = input[13]
    P5.MV502.DI_ZSO = input[14]
    P5.MV502.DI_ZSC = input[15]
    P5.MV503.DI_ZSO = input[16]
    P5.MV503.DI_ZSC = input[17]
    P5.MV504.DI_ZSO = input[18]
    P5.MV504.DI_ZSC = input[19]

    P1.P101.DI_Run = input[20]
    P1.P102.DI_Run = input[21]
    P3.P301.DI_Run = input[22]
    P3.P302.DI_Run = input[23]
    P4.P401.DI_Run = input[24]
    P4.P402.DI_Run = input[25]
    P5.P501.DI_Run = input[26]
    P5.P502.DI_Run = input[27]
    P6.P601.DI_Run = input[28]
    P6.P602.DI_Run = input[29]


def print_plc1_input(HMI):
    # print "HMI.PLANT.Start,HMI.PLANT.Stop,HMI.P101.Status,HMI.P102.Status,HMI.MV101.Status,HMI.MV201.Status,HMI.LIT101.AH,HMI.LIT101.AL,HMI.LIT101.AHH,HMI.LIT101.ALL,HMI.LIT301.AH,HMI.LIT301.AL,HMI.LIT301.AHH,HMI.LIT301.ALL"
    plc1_input_vector=[HMI.PLANT.Start,HMI.PLANT.Stop,HMI.P101.Status,HMI.P102.Status,HMI.MV101.Status,HMI.MV201.Status,
                       HMI.LIT101.AH,HMI.LIT101.AL,HMI.LIT101.AHH,HMI.LIT101.ALL,HMI.LIT301.AH,HMI.LIT301.AL,HMI.LIT301.AHH,HMI.LIT301.ALL]
    print (plc1_input_vector)

def assumption(HMI):
    HMI.LIT101.Hty=True
    HMI.LIT301.Hty = True
    HMI.LIT401.Hty = True



# assume that all sensors and actuators are available and healthy and the system starts.
def generate_plc1_input(HMI,p):
    HMI.PLANT.Start=1
    HMI.PLANT.Stop=0
    HMI.P101.Status= random.randint(1,2)
    HMI.P102.Status= 1
    HMI.MV101.Status= random.randint(1,2)
    HMI.MV201.Status= random.randint(1,2)
    LIT101_Pv=random.uniform(0,1200)
    LIT301_Pv=random.uniform(0,1200)
    HMI.LIT101.AH = LIT101_Pv > p["LIT101_AH"]
    HMI.LIT101.AL = LIT101_Pv < p["LIT101_AL"]
    HMI.LIT101.AHH = LIT101_Pv > p["LIT101_AHH"]
    HMI.LIT101.ALL = LIT101_Pv < p["LIT101_ALL"]
    HMI.LIT301.AH = LIT301_Pv > p["LIT301_AH"]
    HMI.LIT301.AL = LIT301_Pv < p["LIT301_AL"]
    HMI.LIT301.AHH = LIT301_Pv > p["LIT301_AHH"]
    HMI.LIT301.ALL = LIT301_Pv < p["LIT301_ALL"]
    plc1_input_vector = [HMI.PLANT.Start, HMI.PLANT.Stop, HMI.P101.Status, HMI.P102.Status, HMI.MV101.Status,
                         HMI.MV201.Status,
                         HMI.LIT101.AH, HMI.LIT101.AL, HMI.LIT101.AHH, HMI.LIT101.ALL, HMI.LIT301.AH, HMI.LIT301.AL,
                         HMI.LIT301.AHH, HMI.LIT301.ALL]
    print (plc1_input_vector)
    return plc1_input_vector

def test_plc1_input(HMI):
    plc1_input_vector= [1, 0, 1, 1, 1, 2, False, False, False, False, False, True, False, False]
    HMI.PLANT.Start = plc1_input_vector[0]
    HMI.PLANT.Stop = plc1_input_vector[1]
    HMI.P101.Status= plc1_input_vector[2]
    HMI.P102.Status= plc1_input_vector[3]
    HMI.MV101.Status= plc1_input_vector[4]
    HMI.MV201.Status= plc1_input_vector[5]
    HMI.P1.State=2
    # P1.LIT101.AI_Value = usl(800)
    # P3.LIT301.AI_Value = usl(700)
    # HMI.LIT101.Pv=usl(800)
    # HMI.LIT301.Pv = usl(700)
    HMI.LIT101.AH = plc1_input_vector[6]
    HMI.LIT101.AL = plc1_input_vector[7]
    HMI.LIT101.AHH = plc1_input_vector[8]
    HMI.LIT101.ALL = plc1_input_vector[9]
    HMI.LIT301.AH = plc1_input_vector[10]
    HMI.LIT301.AL = plc1_input_vector[11]
    HMI.LIT301.AHH = plc1_input_vector[12]
    HMI.LIT301.ALL = plc1_input_vector[13]

    print (plc1_input_vector)


def print_plc1_output(P1):
    # print "P1.MV101.DO_Open"
    # print P1.MV101.DO_Open
    # print "P1.MV101.DO_Close"
    # print P1.MV101.DO_Close
    # print "P1.P101.DO_Start"
    # print P1.P101.DO_Start
    # print "P1.P102.DO_Start"
    # print P1.P102.DO_Start
    plc1_output_vector=[P1.MV101.DO_Open,P1.MV101.DO_Close,P1.P101.DO_Start,P1.P102.DO_Start]
    # print (plc1_output_vector)
    return plc1_output_vector

def print_plc1_state(HMI):
    plc1_state=[HMI.P101.Status,HMI.P102.Status,HMI.MV101.Status,HMI.MV201.Status]
    print (plc1_state)

def generate_plc2_input(HMI,p):
    pass
def print_plc2_input(HMI):
    pass
def print_plc2_output(P2):
    plc2_output_vector = [P2.MV201.DO_Open, P2.MV201.DO_Close, P2.P201.DO_Start, P2.P202.DO_Start]
    print (plc2_output_vector)
    return plc2_output_vector


def print_plc3_input(HMI):
    pass
def print_plc3_output(P3):
    pass



def print_plc4_input(HMI):
    pass
def print_plc4_output(P4):
    pass



def print_plc5_input(HMI):
    pass
def print_plc5_output(P5):
    pass




def print_plc6_input(HMI):
    pass
def print_plc6_output(P6):
    pass

def print_all_output(P1,P2,P3,P4,P5,P6):
    plc1_output_vector = [P1.MV101.DO_Open, P1.MV101.DO_Close, P1.P101.DO_Start, P1.P102.DO_Start]
    plc2_output_vector= [P2.MV201.DO_Open, P2.MV201.DO_Close, P2.P201.DO_Start, P2.P202.DO_Start, P2.P203.DO_Start, P2.P204.DO_Start, P2.P205.DO_Start, P2.P206.DO_Start]
    plc3_output_vector = [P3.MV301.DO_Open, P3.MV301.DO_Close,P3.MV302.DO_Open, P3.MV302.DO_Close,P3.MV303.DO_Open, P3.MV303.DO_Close,P3.MV304.DO_Open, P3.MV304.DO_Close, P3.P301.DO_Start, P3.P302.DO_Start]
    plc4_output_vector = [P4.P401.DO_Start,P4.P402.DO_Start,P4.P403.DO_Start,P4.P404.DO_Start,P4.UV401.DO_Start]
    plc5_output_vector = [P5.MV501.DO_Open,P5.MV501.DO_Close,P5.MV502.DO_Open,P5.MV502.DO_Close,P5.MV503.DO_Open,P5.MV503.DO_Close,P5.MV504.DO_Open,P5.MV504.DO_Close]
    plc6_output_vector = [P6.P601.DO_Start,P6.P602.DO_Start]
    return plc1_output_vector,plc2_output_vector,plc3_output_vector,plc4_output_vector,plc5_output_vector,plc6_output_vector

# while True:
#     print( random.randint(1,2) )