from SCADA import H
import random
from device.device import *
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

def generate_plc_input(HMI):
    HMI.PLANT.Start = 1
    HMI.PLANT.Stop = 0
    HMI.P1.State=random.randint(1,3)
    HMI.P2.State = random.randint(1, 2)
    HMI.P3.State = random.randint(0, 19)
    if HMI.P3.State==0:
        HMI.P3.State=99
    HMI.P4.State=random.randint(1, 6)
    HMI.P101.Status = random.randint(1,2)
    HMI.P102.Status = 1
    HMI.MV101.Status = random.randint(1,2)
    HMI.MV201.Status = random.randint(1,2)
    HMI.FIT101.Pv = random.uniform(0,3)
    HMI.FIT101.set_alarm()
    HMI.LIT101.Pv = random.uniform(0,1500)
    HMI.LIT101.set_alarm()
    HMI.LIT301.Pv = random.uniform(0,1500)
    HMI.LIT301.set_alarm()
    HMI.LS201.Alarm = random.randint(0,1)
    HMI.LS202.Alarm = random.randint(0,1)
    HMI.LSL203.Alarm = random.randint(0,1)
    HMI.LSLL203.Alarm = random.randint(0,1)
    HMI.P201.Status = random.randint(1,2)
    HMI.P202.Status = 1
    HMI.P203.Status = random.randint(1, 2)
    HMI.P204.Status = 1
    HMI.P205.Status = random.randint(1, 2)
    HMI.P206.Status = 1
    HMI.P207.Status = random.randint(1, 2)
    HMI.P208.Status = 1

    HMI.FIT201.Pv = random.uniform(0.0,4.0)
    HMI.FIT201.set_alarm()
    HMI.AIT201.Pv = random.uniform(0, 950.0)
    HMI.AIT201.set_alarm()
    HMI.AIT202.Pv = random.uniform(0, 12.0)
    HMI.AIT202.set_alarm()
    HMI.AIT203.Pv = random.uniform(0, 750)
    HMI.AIT203.set_alarm()
    HMI.P301.Status = random.randint(1,2)
    HMI.P302.Status = 1

    HMI.FIT301.Pv = random.uniform(0.0, 4.0)
    HMI.FIT301.set_alarm()


    HMI.PSH301.Alarm = random.randint(0,1)
    HMI.DPSH301.Alarm = random.randint(0,1)
    HMI.DPIT301.Pv = random.uniform(0, 120)
    HMI.DPIT301.set_alarm()
    HMI.MV301.Status = random.randint(1,2)
    HMI.MV302.Status = random.randint(1,2)
    HMI.MV303.Status = random.randint(1,2)
    HMI.MV304.Status = random.randint(1,2)
    # # self.P4



    HMI.LS401.Alarm = random.randint(0,1)
    HMI.LIT401.Pv = random.uniform(0,1500)
    HMI.LIT401.set_alarm()
    HMI.P401.Status = random.randint(1,2)
    HMI.P402.Status = 1
    HMI.P403.Status = random.randint(1, 2)
    HMI.P404.Status = 1
    HMI.UV401.Status = random.randint(1, 2)

    HMI.AIT401.Pv = random.uniform(0,150)
    HMI.AIT401.set_alarm()
    HMI.AIT402.Pv = random.uniform(0,800)
    HMI.AIT402.set_alarm()
    HMI.FIT401.Pv = random.uniform(0,4)
    HMI.FIT401.set_alarm()

    HMI.P5.State = random.randint(1, 2)
    # HMI.AIT501.Pv = df.loc[index,'AIT501.Pv']
    # HMI.AIT502.Pv = df.loc[index,'AIT502.Pv']
    # HMI.AIT503.Pv = df.loc[index,'AIT503.Pv']
    # HMI.AIT504.Pv = df.loc[index,'AIT504.Pv']
    # HMI.PIT501.Pv = df.loc[index,'PIT501.Pv']
    # HMI.PIT502.Pv = df.loc[index, 'PIT502.Pv']
    # HMI.PIT503.Pv = df.loc[index, 'PIT503.Pv']
    # HMI.FIT501.Pv = df.loc[index,'FIT501.Pv']
    # HMI.FIT502.Pv = df.loc[index,'FIT502.Pv']
    # HMI.FIT503.Pv = df.loc[index,'FIT503.Pv']
    # HMI.FIT504.Pv = df.loc[index,'FIT504.Pv']


    HMI.MV501.Status = random.randint(1, 2)
    HMI.MV502.Status = random.randint(1, 2)
    HMI.MV503.Status = random.randint(1, 2)
    HMI.MV504.Status = random.randint(1, 2)
    HMI.P501.Status = random.randint(1, 2)
    HMI.P502.Status = 1

    HMI.LSL601.Alarm = random.randint(0,1)
    HMI.LSL602.Alarm = random.randint(0,1)
    HMI.LSL603.Alarm = random.randint(0,1)
    HMI.LSH601.Alarm = random.randint(0,1)
    HMI.LSH602.Alarm = random.randint(0,1)
    HMI.LSH603.Alarm = random.randint(0,1)
    HMI.P601.Status = random.randint(1, 2)
    HMI.P602.Status = random.randint(1, 2)
    HMI.P603.Status = random.randint(1, 2)
    # HMI.FIT601.Pv = df.loc[index,'FIT601.Pv']

def get_all_input(HMI):

    input_vector=[HMI.P1.State,HMI.P2.State,HMI.P3.State,HMI.P4.State,HMI.P101.Status,HMI.P102.Status,HMI.MV101.Status,HMI.MV201.Status,
    HMI.FIT101.AHH, HMI.FIT101.AH, HMI.FIT101.AL, HMI.FIT101.ALL, HMI.LIT101.AHH,HMI.LIT101.AH,HMI.LIT101.AL,HMI.LIT101.ALL,
    HMI.LS201.Alarm, HMI.LS202.Alarm, HMI.LSL203.Alarm, HMI.LSLL203.Alarm, HMI.P201.Status, HMI.P202.Status, HMI.P203.Status,
    HMI.P204.Status,HMI.P205.Status,HMI.P206.Status,HMI.P207.Status,HMI.P208.Status,HMI.FIT201.AHH,HMI.FIT201.AH,HMI.FIT201.AL,HMI.FIT201.ALL,
    HMI.AIT201.AHH, HMI.AIT201.AH,HMI.AIT201.AL,HMI.AIT201.ALL, HMI.AIT202.AHH, HMI.AIT202.AH,HMI.AIT202.AL,HMI.AIT202.ALL,
    HMI.AIT203.AHH, HMI.AIT203.AH,HMI.AIT203.AL,HMI.AIT203.ALL, HMI.P301.Status, HMI.P302.Status,HMI.FIT301.AHH, HMI.FIT301.AH,
    HMI.FIT301.AL,HMI.FIT301.ALL, HMI.LIT301.AHH, HMI.LIT301.AH, HMI.LIT301.AL, HMI.LIT301.ALL, HMI.PSH301.Alarm,HMI.DPSH301.Alarm,
    HMI.DPIT301.AHH, HMI.DPIT301.AH, HMI.DPIT301.AL, HMI.DPIT301.ALL, HMI.MV301.Status,HMI.MV302.Status,HMI.MV303.Status,HMI.MV304.Status,
    HMI.LS401.Alarm,HMI.LIT401.AHH,HMI.LIT401.AH,HMI.LIT401.AL,HMI.LIT401.ALL, HMI.P401.Status, HMI.P402.Status, HMI.P403.Status,  HMI.P404.Status,
    HMI.UV401.Status,HMI.AIT401.AHH,HMI.AIT401.AH,HMI.AIT401.AL,HMI.AIT401.ALL,HMI.AIT402.AHH,HMI.AIT402.AH,HMI.AIT402.AL,HMI.AIT402.ALL,
    HMI.FIT401.AHH, HMI.FIT401.AH, HMI.FIT401.AL, HMI.FIT401.ALL, HMI.MV501.Status, HMI.MV502.Status, HMI.MV503.Status, HMI.MV504.Status, HMI.P501.Status,
    HMI.P502.Status, HMI.LSL601.Alarm, HMI.LSL602.Alarm, HMI.LSL603.Alarm, HMI.LSH601.Alarm, HMI.LSH602.Alarm, HMI.LSH603.Alarm,
    HMI.P601.Status, HMI.P602.Status, HMI.P603.Status]

    return input_vector


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


