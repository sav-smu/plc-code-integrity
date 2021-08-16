# We write plant odes here. The plant would "read" the IO from PLC and decide
# the set of ode functions it follows in the specific current 5 ms period.
from scipy.integrate import odeint
from device.device import *
import random
class plant:
    def __init__(self,maxstep):

        init=[0.0,0.0,550+100*random.random(),550+100*random.random(),550+100*random.random(),200,200]
        self.result=[[0 for x in range(7)] for x in range(maxstep+1)]
        self.result[0] = init
        self.test1=0
        self.test2=0

    def Actuator(self, P1, P2, P3, P4, P5, P6): # Viewer should be notified that passing the output value from plc directly
        # to the input value(return value) is not quite true. For actuators
        # (in here, we are talking about motor valve, pump, pressure pump and ultra violet),
        # the behavior is unkown, it could take seconds for the actuators
        # to process the insctruction, meaning there's a lapse
        #  between the instruction sent and carried out.                --PF
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

        # IO_output=[P1.MV101.DI_ZSO,P1.MV101.DI_ZSC
        # ,P2.MV201.DI_ZSO
        # ,P2.MV201.DI_ZSC
        # ,P3.MV301.DI_ZSO
        # ,P3.MV301.DI_ZSC
        # ,P3.MV302.DI_ZSO
        # ,P3.MV302.DI_ZSC
        # ,P3.MV303.DI_ZSO
        # ,P3.MV303.DI_ZSC
        # ,P3.MV304.DI_ZSO
        # ,P3.MV304.DI_ZSC
        # ,P5.MV501.DI_ZSO
        # ,P5.MV501.DI_ZSC
        # ,P5.MV502.DI_ZSO
        # ,P5.MV502.DI_ZSC
        # ,P5.MV503.DI_ZSO
        # ,P5.MV503.DI_ZSC
        # ,P5.MV504.DI_ZSO
        # ,P5.MV504.DI_ZSC
        # ,P1.P101.DI_Run
        # ,P1.P102.DI_Run
        # ,P3.P301.DI_Run
        # ,P3.P302.DI_Run
        # ,P4.P401.DI_Run
        # ,P4.P402.DI_Run
        # ,P5.P501.DI_Run
        # ,P5.P502.DI_Run
        # ,P6.P601.DI_Run
        # ,P6.P602.DI_Run ]
        # print IO_output

    def Plant(self, P1, P2, P3, P4, P5, P6,k): #k is the total steps counted every 5 ms   --PF
# The ODEs should be reset to 0 after 1 cycle --PF Jan 25
        self.time_UF="y0=0"
        self.time_RO="y1=0"
        self.h_t101="y2=0"
        self.h_t301="y3=0"
        self.h_t401="y4=0"
        self.h_t601="y5=0"
        self.h_t602="y6=0"


        self.p = {"f_mv101":2.3*1000000000/3600,"S_t101":1.5*1000000,"S_t301":1.5*1000000,"S_t401":1.5*1000000,"S_t601":1.5*1000000,"S_t601":1.5*1000000,"S_t602":1.5*1000000,"f_p101":2.0*1000000000/3600,"f_mv201":2.0*1000000000/3600,"f_p301":2.0*1000000000/3600,"f_mv302":2.0*1000000000/3600,"f_p602":2.0*1000000000/3600,"f_p401":2.0*1000000000/36001,"f_mv501":2.0*1000000000/3600,"f_mv502":0.00006111,"f_mv503":0.00049,"f_p601":2.0*1000000000/36001,"LIT101_AL":0.2,"LIT101_AH":0.8,"LIT301_AL":0.2,"LIT301_AH":0.8,"LIT401_AL":0.2,"LIT401_AH":0.8,"LIT601_AL":0.2,"LIT601_AH":0.8,"LIT602_AL":0.2,"LIT602_AH":0.8,"cond_AIT201_AL":250,"cond_AIT201_AH":260,"ph_AIT202_AL":6.95,"ph_AIT202_AH":7.05,"orp_AIT203_AL":420,"orp_AIT203_AH":500,"cond_AIT503_AH":260,"h201_AL":50,"h202_AL":4,"h203_AL":15,"cond_AIT503_AL":250,"cond_AIT503_AH":260,"orp_AIT402_AL":420,"orp_AIT402_AH":500,"omega_inlet":0.001}  # critical plant parameters
#		print "INITs of of the tank at the start of 0 second"
#		print "Level of Tank 101: %s meter"%str(result[0][2])[:5]
#		print "Level of Tank 301: %s meter"%str(result[0][3])[:5]
#		print "Level of Tank 401: %s meter"%str(result[0][4])[:5]
#		print "Level of Tank 601: %s meter"%str(result[0][5])[:5]
#		print "Level of Tank 602: %s meter"%str(result[0][6])[:5]
#		print "\n Simulating...\n"

        if P1.MV101.DI_ZSO == 1:
            self.h_t101+="+self.p['f_mv101'] / self.p['S_t101']"
        if P1.P101.DI_Run == 1 or P1.P102.DI_Run == 1: #P101, drawing water from tank101
            self.h_t101+="-self.p['f_p101'] / self.p['S_t101']"

        if P2.MV201.DI_ZSO == 1 and P1.P101.DI_Run == 1:#mv201, feeding water to tank301
            self.h_t301+="+self.p['f_mv201'] / self.p['S_t301']"

        if P3.P301.DI_Run == 1 or P3.P302.DI_Run == 1: #p301, drawing water from tank301
            self.h_t301+="-self.p['f_p301'] / self.p['S_t301']"


        if P3.P301.DI_Run == 1 or P3.P302.DI_Run == 1 and P3.MV301.DI_ZSC and  P3.MV302.DI_ZSC and P3.MV303.DI_ZSC and P3.MV304.DO_ZSO and P6.P602.DI_Run == 0: #UF flushing procedure, 30 sec
            self.h_t401+=""
            self.time_UF+='1'
        if P3.P301.DI_Run == 1 or P3.P302.DI_Run == 1 and P3.MV301.DI_ZSC == 1 and  P3.MV302.DI_ZSO == 1 and P3.MV303.DI_ZSC == 1 and P3.MV304.DI_ZSC == 1 and P6.P602.DI_Run == 0:   #UF ultra filtration procedure, 30 min
            self.h_t401+="+ self.p['f_mv302'] / self.p['S_t401']"
            self.time_UF += '1'
        if P3.P301.DI_Run == 0 and P3.P302.DI_Run == 0 and P3.MV301.DI_ZSO == 1 and  P3.MV302.DI_ZSC == 1 and P3.MV303.DI_ZSO == 1 and P3.MV304.DI_ZSC == 1 and P6.P602.DI_Run == 1:   #UF back wash procedure, 45 sec
            self.h_t602+="- self.p['f_p602'] / self.p['S_t602']"
            self.time_UF+= '1'
        if P3.P301.DI_Run == 0 and P3.P302.DI_Run == 0 and P3.MV301.DI_ZSC == 1 and  P3.MV302.DI_ZSC == 1 and P3.MV303.DI_ZSC == 1 and P3.MV304.DI_ZSO == 1 and P6.P602.DI_Run == 0:   #UF feed tank draining procedure, 1 min
            self.h_t401+=""
            self.time_UF += '1'
        #else:
        #	self.time_UF += '' #Ultra Filtration doesn't count time when not in procedures.

        if P4.P401.DI_Run == 1 or P4.P402.DI_Run == 1: #P401, drawing water from t401
            self.h_t401+="- self.p['f_p401'] / self.p['S_t401']"
        if P4.P401.DI_Run == 1 or P4.P402.DI_Run == 1 and P5.P501.DI_Run == 1 or P5.P502.DI_Run == 1 and P5.MV501.DI_ZSO == 1 and P5.MV502.DI_ZSO == 1 and P5.MV503.DI_ZSC == 1 and P5.MV504.DI_ZSC == 1:#procedure for RO normal functioning with product of permeate 60% and backwash 40%
            self.h_t601+="+self.p['f_mv501'] / self.p['S_t601']"
            self.h_t602+="+self.p['f_mv502'] / self.p['S_t602']"
            self.time_RO += ''
        elif P4.P401.DI_Run == 1 or P4.P402.DI_Run == 1 and P5.P501.DI_Run == 1 or P5.P502.DI_Run == 1 and P5.MV501.DI_ZSC == 1 and P5.MV502.DI_ZSC == 1 and P5.MV503.DI_ZSO == 1 and P5.MV504.DI_ZSO == 1:#procedure for RO flushing with product of backwash 60% and drain 40%
            self.h_t602+="+self.p['f_mv503'] / self.p['S_t602']"
            self.time_RO += ''
        else:
            self.time_RO += '' #Reverse Osmisis doesn't count time when not in procedure
        if P6.P601.DI_Run == 1: # Pumping water out of tank601
            self.h_t601+="-self.p['f_p601'] / self.p['S_t601']"

        self.result[k+1] = odeint(self.func,self.result[k],[0,0.005])[1]


# converting physical value to sensor return values
        P1.LIT101.W_AI_Value = usl_w(self.result[k+1][2])
        P3.LIT301.W_AI_Value = usl_w(self.result[k+1][3])
        P4.LIT401.W_AI_Value = usl_w(self.result[k+1][4])

        P1.LIT101.AI_Value = usl(self.result[k+1][2])
        P3.LIT301.AI_Value = usl(self.result[k+1][3])
        P4.LIT401.AI_Value = usl(self.result[k+1][4])

        P6.LSL601.DI_LS = self.result[k+1][5]<self.p["LIT601_AL"]
        P6.LSH601.DI_LS = self.result[k+1][5]>self.p["LIT601_AH"]
        P6.LSL602.DI_LS = self.result[k+1][6]<self.p["LIT601_AL"]
        P6.LSH602.DI_LS = self.result[k+1][6]>self.p["LIT601_AH"]

    def func(self,y,t):
        exec self.time_UF
        exec self.time_RO
        exec self.h_t101
        exec self.h_t301
        exec self.h_t401
        exec self.h_t601
        exec self.h_t602
        return y0,y1,y2,y3,y4,y5,y6

#Yuqi, Ping-Fan
