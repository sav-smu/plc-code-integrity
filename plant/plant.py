from device.device import *
import random
class plant:
    def __init__(self):
        self.test=0
    def Actuator(self, P1, P2, P3, P4, P5, P6):
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
