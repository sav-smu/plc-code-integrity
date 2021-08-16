import os
import pandas as pd

def alarm_transfer(alarm):
    if alarm=='Inactive':
        return 0
    else:
        return 1


def get_plc1_input(df,HMI,index,p):
    HMI.PLANT.Start=1
    HMI.PLANT.Stop=0
    HMI.P1.State = 2
    HMI.P101.Status = df.loc[index,'P101.Status']
    HMI.P102.Status = df.loc[index,'P102.Status']
    HMI.MV101.Status= df.loc[index,'MV101.Status']
    HMI.MV201.Status= df.loc[index,'MV201.Status']
    LIT101_Pv=df.loc[index,'LIT101.Pv']
    LIT301_Pv=df.loc[index,'LIT301.Pv']
    HMI.LIT101.AH = LIT101_Pv > p["LIT101_AH"]
    HMI.LIT101.AL = LIT101_Pv < p["LIT101_AL"]
    HMI.LIT101.AHH = LIT101_Pv > p["LIT101_AHH"]
    HMI.LIT101.ALL = LIT101_Pv < p["LIT101_ALL"]
    HMI.LIT301.AH = LIT301_Pv > p["LIT301_AH"]
    HMI.LIT301.AL = LIT301_Pv < p["LIT301_AL"]
    HMI.LIT301.AHH = LIT301_Pv > p["LIT301_AHH"]
    HMI.LIT301.ALL = LIT301_Pv < p["LIT301_ALL"]
    plc1_input_vector = [HMI.P101.Status, HMI.P102.Status, HMI.MV101.Status,HMI.MV201.Status,HMI.LIT101.AH, HMI.LIT101.AL, HMI.LIT101.AHH, HMI.LIT101.ALL, HMI.LIT301.AH, HMI.LIT301.AL,HMI.LIT301.AHH, HMI.LIT301.ALL]
    # print (plc1_input_vector)
    return plc1_input_vector

def get_plc_input(df,HMI,index):
    HMI.PLANT.Start=1
    HMI.PLANT.Stop=0
    HMI.P1.State = df.loc[index,'P1_STATE']
    HMI.P101.Status = df.loc[index,'P101.Status']
    HMI.P102.Status = df.loc[index,'P102.Status']
    HMI.MV101.Status= df.loc[index,'MV101.Status']
    HMI.LIT101.Pv=df.loc[index,'LIT101.Pv']
    HMI.LIT101.set_alarm()
    HMI.FIT101.Pv=df.loc[index,'FIT101.Pv']
    HMI.FIT101.set_alarm()

    HMI.P2.State = df.loc[index,'P2_STATE']
    HMI.MV201.Status= df.loc[index,'MV201.Status']
    HMI.LS201.Alarm = alarm_transfer(df.loc[index,'LS201.Alarm'])
    HMI.LS202.Alarm = alarm_transfer(df.loc[index,'LS202.Alarm'])
    HMI.LSL203.Alarm = alarm_transfer(df.loc[index,'LSL203.Alarm'])
    HMI.LSLL203.Alarm = alarm_transfer(df.loc[index,'LSLL203.Alarm'])
    HMI.P201.Status = df.loc[index,'P201.Status']
    HMI.P202.Status = df.loc[index,'P202.Status']
    HMI.P203.Status = df.loc[index,'P203.Status']
    HMI.P204.Status = df.loc[index,'P204.Status']
    HMI.P205.Status = df.loc[index,'P205.Status']
    HMI.P206.Status = df.loc[index,'P206.Status']
    HMI.P207.Status = df.loc[index,'P207.Status']
    HMI.P208.Status = df.loc[index,'P208.Status']

    HMI.FIT201.Pv = df.loc[index,'FIT201.Pv']
    HMI.FIT201.set_alarm()
    HMI.AIT201.Pv = df.loc[index,'AIT201.Pv']
    HMI.AIT201.set_alarm()
    HMI.AIT202.Pv = df.loc[index,'AIT202.Pv']
    HMI.AIT202.set_alarm()
    HMI.AIT203.Pv = df.loc[index,'AIT203.Pv']
    HMI.AIT203.set_alarm()

    HMI.P3.State = df.loc[index, 'P3_STATE']
    HMI.LIT301.Pv=df.loc[index,'LIT301.Pv']
    HMI.LIT301.set_alarm()

    HMI.P301.Status = df.loc[index,'P301.Status']
    HMI.P302.Status = df.loc[index,'P302.Status']

    HMI.FIT301.Pv = df.loc[index,'FIT301.Pv']
    HMI.FIT301.set_alarm()


    HMI.PSH301.Alarm = alarm_transfer(df.loc[index,'PSH301.Alarm'])
    HMI.DPSH301.Alarm = alarm_transfer(df.loc[index,'DPSH301.Alarm'])
    HMI.DPIT301.Pv = df.loc[index,'DPIT301.Pv']
    HMI.DPIT301.set_alarm()
    HMI.MV301.Status = df.loc[index,'MV301.Status']
    HMI.MV302.Status = df.loc[index,'MV302.Status']
    HMI.MV303.Status = df.loc[index,'MV303.Status']
    HMI.MV304.Status = df.loc[index,'MV304.Status']
    # # self.P4

    HMI.P4.State = df.loc[index, 'P4_STATE']
    HMI.LS401.Alarm = alarm_transfer(df.loc[index,'LS401.Alarm'])
    HMI.LIT401.Pv = df.loc[index,'LIT401.Pv']
    HMI.LIT401.set_alarm()
    HMI.P401.Status = df.loc[index,'P401.Status']
    HMI.P402.Status = df.loc[index,'P402.Status']
    HMI.P403.Status = df.loc[index,'P403.Status']
    HMI.P404.Status = df.loc[index,'P404.Status']
    HMI.UV401.Status = df.loc[index,'UV401.Status']

    HMI.AIT401.Pv = df.loc[index,'AIT401.Pv']
    HMI.AIT401.set_alarm()
    HMI.AIT402.Pv = df.loc[index,'AIT402.Pv']
    HMI.AIT402.set_alarm()
    HMI.FIT401.Pv = df.loc[index,'FIT401.Pv']
    HMI.FIT401.set_alarm()

    HMI.P5.State = df.loc[index, 'P5_STATE']
    HMI.AIT501.Pv = df.loc[index,'AIT501.Pv']
    HMI.AIT502.Pv = df.loc[index,'AIT502.Pv']
    HMI.AIT503.Pv = df.loc[index,'AIT503.Pv']
    HMI.AIT504.Pv = df.loc[index,'AIT504.Pv']
    HMI.PIT501.Pv = df.loc[index,'PIT501.Pv']
    HMI.PIT502.Pv = df.loc[index, 'PIT502.Pv']
    HMI.PIT503.Pv = df.loc[index, 'PIT503.Pv']
    HMI.FIT501.Pv = df.loc[index,'FIT501.Pv']
    HMI.FIT502.Pv = df.loc[index,'FIT502.Pv']
    HMI.FIT503.Pv = df.loc[index,'FIT503.Pv']
    HMI.FIT504.Pv = df.loc[index,'FIT504.Pv']


    HMI.MV501.Status = df.loc[index,'MV501.Status']
    HMI.MV502.Status = df.loc[index,'MV502.Status']
    HMI.MV503.Status = df.loc[index,'MV503.Status']
    HMI.MV504.Status = df.loc[index,'MV504.Status']
    HMI.P501.Status = df.loc[index,'P501.Status']
    HMI.P502.Status = df.loc[index,'P502.Status']

    HMI.P6.State = df.loc[index,'P6_STATE']
    HMI.LSL601.Alarm = alarm_transfer(df.loc[index,'LSL601.Alarm'])
    HMI.LSL602.Alarm = alarm_transfer(df.loc[index, 'LSL602.Alarm'])
    HMI.LSL603.Alarm = alarm_transfer(df.loc[index, 'LSL603.Alarm'])
    HMI.LSH601.Alarm = alarm_transfer(df.loc[index, 'LSH601.Alarm'])
    HMI.LSH602.Alarm = alarm_transfer(df.loc[index, 'LSH602.Alarm'])
    HMI.LSH603.Alarm = alarm_transfer(df.loc[index, 'LSH603.Alarm'])
    HMI.P601.Status = df.loc[index,'P601.Status']
    HMI.P602.Status = df.loc[index, 'P602.Status']
    HMI.P603.Status = df.loc[index, 'P603.Status']
    HMI.FIT601.Pv = df.loc[index,'FIT601.Pv']


    # plc1_input_vector = [HMI.P101.Status, HMI.P102.Status, HMI.MV101.Status,HMI.MV201.Status,HMI.LIT101.AH, HMI.LIT101.AL, HMI.LIT101.AHH, HMI.LIT101.ALL, HMI.LIT301.AH, HMI.LIT301.AL,HMI.LIT301.AHH, HMI.LIT301.ALL]
    # # print (plc1_input_vector)
    return True

# input_path=os.path.abspath('..')+"/data/22June2020_B.csv"
# # out_path=os.path.abspath('..')+"\data\\22June2020_PLC1.csv"
# df=pd.read_csv(input_path)
#
# print (alarm_transfer(df.loc[0,'LS201.Alarm']))
# Index(['t_stamp', 'P1_STATE', 'LIT101.Pv', 'FIT101.Pv', 'MV101.Status',
      #  'P101.Status', 'P102.Status', 'P2_STATE', 'FIT201.Pv', 'AIT201.Pv',
      #  'AIT202.Pv', 'AIT203.Pv', 'MV201.Status', 'P201.Status', 'P202.Status',
      #  'P203.Status', 'P204.Status', 'P205.Status', 'P206.Status',
      #  'P207.Status', 'P208.Status', 'LS201.Alarm', 'LS202.Alarm',
      #  'LSL203.Alarm', 'LSLL203.Alarm', 'P3_STATE', 'AIT301.Pv', 'AIT302.Pv',
      #  'AIT303.Pv', 'LIT301.Pv', 'FIT301.Pv', 'DPIT301.Pv', 'MV301.Status',
      #  'MV302.Status', 'MV303.Status', 'MV304.Status', 'P301.Status',
      #  'P302.Status', 'PSH301.Alarm', 'DPSH301.Alarm', 'P4_STATE', 'LIT401.Pv',
      #  'FIT401.Pv', 'AIT401.Pv', 'AIT402.Pv', 'P401.Status', 'P402.Status',
      #  'P403.Status', 'P404.Status', 'UV401.Status', 'LS401.Alarm', 'P5_STATE',
      #  'FIT501.Pv', 'FIT502.Pv', 'FIT503.Pv', 'FIT504.Pv', 'AIT501.Pv',
      #  'AIT502.Pv', 'AIT503.Pv', 'AIT504.Pv', 'PIT501.Pv', 'PIT502.Pv',
      #  'PIT503.Pv', 'P501.Status', 'P502.Status', 'MV501.Status',
      #  'MV502.Status', 'MV503.Status', 'MV504.Status', 'PSH501.Alarm',
      #  'PSL501.Alarm', 'P6_STATE', 'FIT601.Pv', 'P601.Status', 'P602.Status',
      #  'P603.Status', 'LSH601.Alarm', 'LSL601.Alarm', 'LSH602.Alarm',
      #  'LSL602.Alarm', 'LSH603.Alarm', 'LSL603.Alarm'],
      # dtype='object')
