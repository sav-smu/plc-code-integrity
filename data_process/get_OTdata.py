import pandas as pd
import os
from SCADA import H

def get_OTinput(df,HMI,index):
    HMI.PLANT.Start=1
    HMI.PLANT.Stop=0
    HMI.P1.State = df.loc[index,'PLC1']
    # print (HMI.P1.State)
    HMI.P101.Status = df.loc[index,'P101']
    HMI.P102.Status = df.loc[index,'P102']
    HMI.MV101.Status= df.loc[index,'MV101']
    HMI.MV201.Status= df.loc[index,'MV201']
    HMI.FIT101.Pv = df.loc[index,'FIT101']
    # print (HMI.FIT101.Pv)
    HMI.FIT101.set_alarm()
    HMI.LIT101.Pv = df.loc[index,'LIT101']
    # print (HMI.LIT101.Pv)
    HMI.LIT101.set_alarm()
    HMI.LIT301.Pv = df.loc[index,'LIT301']
    # print(HMI.LIT301.Pv)
    HMI.LIT301.set_alarm()

    HMI.P2.State = df.loc[index,'PLC2']
    HMI.MV201.Status= df.loc[index,'MV201']
    HMI.P201.Status = df.loc[index,'P201']
    HMI.P202.Status = df.loc[index,'P202']
    HMI.P203.Status = df.loc[index,'P203']
    HMI.P204.Status = df.loc[index,'P204']
    HMI.P205.Status = df.loc[index,'P205']
    HMI.P206.Status = df.loc[index,'P206']
    # HMI.P207.Status = df.loc[index,'P207']
    # HMI.P208.Status = df.loc[index,'P208']

    HMI.FIT201.Pv = df.loc[index,'FIT201']
    HMI.FIT201.set_alarm()
    HMI.AIT201.Pv = df.loc[index,'AIT201']
    HMI.AIT201.set_alarm()
    HMI.AIT202.Pv = df.loc[index,'AIT202']
    HMI.AIT202.set_alarm()
    HMI.AIT203.Pv = df.loc[index,'AIT203']
    HMI.AIT203.set_alarm()

    HMI.P3.State = df.loc[index, 'PLC3']
    HMI.LIT301.Pv=df.loc[index,'LIT301']
    HMI.LIT301.set_alarm()

    HMI.P301.Status = df.loc[index,'P301']
    HMI.P302.Status = df.loc[index,'P302']

    HMI.FIT301.Pv = df.loc[index,'FIT301']
    HMI.FIT301.set_alarm()



    HMI.MV301.Status = df.loc[index,'MV301']
    HMI.MV302.Status = df.loc[index,'MV302']
    HMI.MV303.Status = df.loc[index,'MV303']
    HMI.MV304.Status = df.loc[index,'MV304']
    # # self.P4

    HMI.P4.State = df.loc[index, 'PLC4']
    HMI.LIT401.Pv = df.loc[index,'LIT401']
    HMI.LIT401.set_alarm()
    HMI.P401.Status = df.loc[index,'P401']
    HMI.P402.Status = df.loc[index,'P402']
    HMI.P403.Status = df.loc[index,'P403']
    HMI.P404.Status = df.loc[index,'P404']
    HMI.UV401.Status = df.loc[index,'UV401']

    HMI.AIT401.Pv = df.loc[index,'AIT401']
    HMI.AIT401.set_alarm()
    HMI.AIT402.Pv = df.loc[index,'AIT402']
    HMI.AIT402.set_alarm()
    HMI.FIT401.Pv = df.loc[index,'FIT401']
    HMI.FIT401.set_alarm()

    HMI.P5.State = df.loc[index, 'PLC5']
    HMI.AIT501.Pv = df.loc[index,'AIT501']
    HMI.AIT502.Pv = df.loc[index,'AIT502']
    HMI.AIT503.Pv = df.loc[index,'AIT503']
    HMI.AIT504.Pv = df.loc[index,'AIT504']
    HMI.PIT501.Pv = df.loc[index,'PIT501']
    HMI.PIT502.Pv = df.loc[index, 'PIT502']
    HMI.PIT503.Pv = df.loc[index, 'PIT503']
    HMI.FIT501.Pv = df.loc[index,'FIT501']
    HMI.FIT502.Pv = df.loc[index,'FIT502']
    HMI.FIT503.Pv = df.loc[index,'FIT503']
    HMI.FIT504.Pv = df.loc[index,'FIT504']


    HMI.MV501.Status = df.loc[index,'MV501']
    HMI.MV502.Status = df.loc[index,'MV502']
    HMI.MV503.Status = df.loc[index,'MV503']
    HMI.MV504.Status = df.loc[index,'MV504']
    HMI.P501.Status = df.loc[index,'P501']
    HMI.P502.Status = df.loc[index,'P502']

    HMI.P6.State = df.loc[index,'PLC6']
    HMI.P601.Status = df.loc[index,'P601']
    HMI.P602.Status = df.loc[index, 'P602']
    HMI.P603.Status = df.loc[index, 'P603']
    HMI.FIT601.Pv = df.loc[index,'FIT601']




# input_path=os.path.abspath('..')+"/data/CISS2020-OL.July27_Attestor.xlsx"
# df=pd.read_excel(input_path)


# Index(['Timestamp', 'Annotation', 'Other Anomalies', 'A#Attester', 'FIT101',
#        'LIT101', 'MV101', 'P102', 'P101', 'AIT202', 'AIT203', 'AIT201',
#        'FIT201', 'MV201', 'P206', 'P204', 'P205', 'P203', 'P202', 'P201',
#        'AIT301', 'AIT302', 'AIT303', 'DPIT301', 'FIT301', 'LIT301', 'MV301',
#        'MV302', 'MV304', 'MV303', 'P301', 'P302', 'AIT402', 'AIT401', 'FIT401',
#        'LIT401', 'P402', 'P403', 'P404', 'P401', 'UV401', 'AIT501', 'AIT502',
#        'AIT503', 'AIT504', 'FIT503', 'FIT502', 'FIT504', 'FIT501', 'MV504',
#        'MV503', 'MV501', 'MV502', 'P501', 'P502', 'PIT501', 'PIT502', 'PIT503',
#        'FIT601', 'P601', 'P602', 'P603', 'PLC4', 'PLC1', 'PLC6', 'PLC5',
#        'PLC3', 'PLC2', 'P1SA1', 'Plant'],
#       dtype='object')