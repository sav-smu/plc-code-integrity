from plc import plc1,plc2,plc3,plc4,plc5,plc6
import sys,os
sys.path.insert(0,os.getcwd())
from SCADA import H
from IO import *
from PLC_simulation import plc_simulation
import time
from plantio.client import (
    Client,GroupOutputAdapter, Plant, PLC, FIT, LIT, AIT, PIT, Pump, MV, UV, PSH, DPIT, DPSH)

oa = GroupOutputAdapter("attester", remote=True,host="192.168.1.234")
sa_client = Client(cache_time_limit=0.1)
# Initiating Plant
# Defining I/O
IO_DI_WIFI = DI_WIFI()
IO_P1 = P1()
IO_P2 = P2()
IO_P3 = P3()
IO_P4 = P4()
IO_P5 = P5()
IO_P6 = P6()
print ("Initializing SCADA HMI")
HMI = H()
print ("Initializing PLCs\n")
PLC1 = plc1.plc1(HMI)
PLC2 = plc2.plc2(HMI)
PLC3 = plc3.plc3(HMI)
PLC4 = plc4.plc4(HMI)
PLC5 = plc5.plc5(HMI)
PLC6 = plc6.plc6(HMI)
print ("Now starting Simulation")
# Main Loop Body
plant = Plant()
p1 = PLC(1)
lit101 = LIT(1, 101)
fit101 = FIT(1, 101)
mv101 = MV(1, 101)
p101 = Pump(1, 101)
p102 = Pump(1, 102)

p2 = PLC(2)
fit201 = FIT(2, 201)
ait201 = AIT(2, 201)
ait202 = AIT(2, 201)
ait203 = AIT(2, 201)
mv201 = MV(2, 201)
p201 = Pump(2, 201)
p202 = Pump(2, 202)
p203 = Pump(2, 203)
p204 = Pump(2, 204)
p205 = Pump(2, 205)
p206 = Pump(2, 206)
LS201_Alarm = 0
LS202_Alarm = 0
LSL203_Alarm = 0
LSLL203_Alarm = 0

p3 = PLC(3)
lit301 = LIT(3, 301)
fit301 = FIT(3, 301)
dpit301 = DPIT(3, 301)
mv301 = MV(3, 301)
mv302 = MV(3, 302)
mv303 = MV(3, 303)
mv304 = MV(3, 304)
p301 = Pump(3, 301)
p302 = Pump(3, 302)
PSH301_Alarm = 0
DPSH301_Alarm = 0

p4 = PLC(4)
lit401 = LIT(4, 401)
fit401 = FIT(4, 401)
ait401 = AIT(4, 401)
ait402 = AIT(4, 402)
p401 = Pump(4, 401)
p402 = Pump(4, 402)
p403 = Pump(4, 403)
p404 = Pump(4, 404)
uv401 = UV(4, 401)
LS401_Alarm = 0

p5 = PLC(5)
fit501 = FIT(5, 501)
fit502 = FIT(5, 502)
fit503 = FIT(5, 503)
fit504 = FIT(5, 504)
ait501 = AIT(5, 501)
ait502 = AIT(5, 502)
ait503 = AIT(5, 503)
ait504 = AIT(5, 504)
pit501 = PIT(5, 501)
pit502 = PIT(5, 502)
pit503 = PIT(5, 503)
p501 = Pump(5, 501)
p502 = Pump(5, 502)
mv501 = MV(5, 501)
mv502 = MV(5, 502)
mv503 = MV(5, 503)
mv504 = MV(5, 504)
PSH501_Alarm = 0
PSL501_Alarm = 0

p6 = PLC(6)
fit601 = FIT(6, 601)
p601 = Pump(6, 601)
p602 = Pump(6, 602)
p603 = Pump(6, 603)

Sec_P=0
Min_P=0
i=0
input=[]
output=[]
# plc_simulation.test_plc1_input(HMI)
while True:
    if plant.start:
        print ("Plant Started ")
        # Use this if you want cached values
        # sa_client = Client(cache_time_limit=0.1)
        # Shares the socket for the different tags
        sa_client.share_client([
            plant, p1, lit101, fit101, mv101, p101, p102, p2, fit201, ait201, ait202, ait203, mv201, p201, p202, p203,
            p204,
            p205, p206, p3, lit301
            , fit301, dpit301, mv301, mv302, mv303, mv304, p301, p302, p4, lit401, fit401, ait401, ait402, p401, p402,
            p403,
            p404, uv401, p5, fit501,
            fit502, fit503, fit504, ait501, ait502, ait503, ait504, pit501, pit502, pit503, p501, p502, mv501, mv502,
            mv503,
            mv504, p6, fit601,
            p601, p603])
        HMI.PLANT.Start = 1
        HMI.PLANT.Stop = 0
        timestamp=lit101.time
        HMI.P1.state = p1.state
        HMI.LIT101.Pv = lit101.value
        HMI.LIT101.AHH = lit101.isHighHigh
        HMI.LIT101.AH = lit101.isHigh
        HMI.LIT101.AL = lit101.isLow
        HMI.LIT101.ALL = lit101.isLowLow

        HMI.FIT101.Pv = fit101.value
        HMI.FIT101.AHH = fit101.isHighHigh
        HMI.FIT101.AH = fit101.isHigh
        HMI.FIT101.AL = fit101.isLow
        HMI.FIT101.ALL = fit101.isLowLow

        HMI.MV101.Status = mv101.value
        HMI.P101.Status = p101.value
        HMI.P102.Status = p102.value

        HMI.P2.state = p2.state

        HMI.FIT201.Pv = fit201.value
        HMI.FIT201.AHH = fit201.isHighHigh
        HMI.FIT201.AH = fit201.isHigh
        HMI.FIT201.AL = fit201.isLow
        HMI.FIT201.ALL = fit201.isLowLow

        HMI.AIT201.Pv = ait201.value
        HMI.AIT201.AHH = ait201.isHighHigh
        HMI.AIT201.AH = ait201.isHigh
        HMI.AIT201.AL = ait201.isLow
        HMI.AIT201.ALL = ait201.isLowLow

        HMI.AIT202.Pv = ait202.value
        HMI.AIT202.AHH = ait202.isHighHigh
        HMI.AIT202.AH = ait202.isHigh
        HMI.AIT202.AL = ait202.isLow
        HMI.AIT202.ALL = ait202.isLowLow

        HMI.AIT203.Pv = ait203.value
        HMI.AIT203.AHH = ait203.isHighHigh
        HMI.AIT203.AH = ait203.isHigh
        HMI.AIT203.AL = ait203.isLow
        HMI.AIT203.ALL = ait203.isLowLow

        HMI.MV201.Status = mv201.value
        HMI.P201.Status = p201.value
        HMI.P202.Status = p202.value
        HMI.P203.Status = p203.value
        HMI.P204.Status = p204.value
        HMI.P205.Status = p205.value
        HMI.P206.Status = p206.value



        HMI.P3.state = p3.state

        HMI.LIT301.Pv = lit301.value
        HMI.LIT301.AHH = lit301.isHighHigh
        HMI.LIT301.AH = lit301.isHigh
        HMI.LIT301.AL = lit301.isLow
        HMI.LIT301.ALL = lit301.isLowLow

        HMI.FIT301.Pv = fit301.value
        HMI.FIT301.AHH = fit301.isHighHigh
        HMI.FIT301.AH = fit301.isHigh
        HMI.FIT301.AL = fit301.isLow
        HMI.FIT301.ALL = fit301.isLowLow

        HMI.DPIT301.Pv=dpit301.value
        HMI.DPIT301.AHH = dpit301.isHighHigh
        HMI.DPIT301.AH = dpit301.isHigh
        HMI.DPIT301.AL = dpit301.isLow
        HMI.DPIT301.ALL = dpit301.isLowLow

        HMI.MV301.Status=mv301.value
        HMI.MV302.Status = mv302.value
        HMI.MV303.Status = mv303.value
        HMI.MV304.Status = mv304.value
        HMI.P301.Status = p301.value
        HMI.P302.Status = p302.value



        HMI.P4.state = p4.state
        HMI.LIT401.Pv = lit401.value
        HMI.LIT401.AHH = lit401.isHighHigh
        HMI.LIT401.AH = lit401.isHigh
        HMI.LIT401.AL = lit401.isLow
        HMI.LIT401.ALL = lit401.isLowLow

        HMI.FIT401.Pv = fit401.value
        HMI.FIT401.AHH = fit401.isHighHigh
        HMI.FIT401.AH = fit401.isHigh
        HMI.FIT401.AL = fit401.isLow
        HMI.FIT401.ALL = fit401.isLowLow

        HMI.AIT401.Pv = ait401.value
        HMI.AIT401.AHH = ait401.isHighHigh
        HMI.AIT401.AH = ait401.isHigh
        HMI.AIT401.AL = ait401.isLow
        HMI.AIT401.ALL = ait401.isLowLow

        HMI.AIT402.Pv = ait402.value
        HMI.AIT402.AHH = ait402.isHighHigh
        HMI.AIT402.AH = ait402.isHigh
        HMI.AIT402.AL = ait402.isLow
        HMI.AIT402.ALL = ait402.isLowLow

        HMI.P401.Status = p401.value
        HMI.P402.Status = p402.value
        HMI.P403.Status = p403.value
        HMI.P404.Status = p404.value
        HMI.UV401.Status = uv401.value



        HMI.P5.state = p5.state
        HMI.FIT501.Pv = fit501.value
        HMI.FIT501.AHH = fit501.isHighHigh
        HMI.FIT501.AH = fit501.isHigh
        HMI.FIT501.AL = fit501.isLow
        HMI.FIT501.ALL = fit501.isLowLow

        HMI.FIT502.Pv = fit502.value
        HMI.FIT502.AHH = fit502.isHighHigh
        HMI.FIT502.AH = fit502.isHigh
        HMI.FIT502.AL = fit502.isLow
        HMI.FIT502.ALL = fit502.isLowLow

        HMI.FIT503.Pv = fit503.value
        HMI.FIT503.AHH = fit503.isHighHigh
        HMI.FIT503.AH = fit503.isHigh
        HMI.FIT503.AL = fit503.isLow
        HMI.FIT503.ALL = fit503.isLowLow

        HMI.FIT504.Pv = fit504.value
        HMI.FIT504.AHH = fit504.isHighHigh
        HMI.FIT504.AH = fit504.isHigh
        HMI.FIT504.AL = fit504.isLow
        HMI.FIT504.ALL = fit504.isLowLow

        HMI.AIT501.Pv = ait501.value
        HMI.AIT501.AHH = ait501.isHighHigh
        HMI.AIT501.AH = ait501.isHigh
        HMI.AIT501.AL = ait501.isLow
        HMI.AIT501.ALL = ait501.isLowLow

        HMI.AIT502.Pv = ait502.value
        HMI.AIT502.AHH = ait502.isHighHigh
        HMI.AIT502.AH = ait502.isHigh
        HMI.AIT502.AL = ait502.isLow
        HMI.AIT502.ALL = ait502.isLowLow

        HMI.AIT503.Pv = ait503.value
        HMI.AIT503.AHH = ait503.isHighHigh
        HMI.AIT503.AH = ait503.isHigh
        HMI.AIT503.AL = ait503.isLow
        HMI.AIT503.ALL = ait503.isLowLow

        HMI.AIT504.Pv = ait504.value
        HMI.AIT504.AHH = ait504.isHighHigh
        HMI.AIT504.AH = ait504.isHigh
        HMI.AIT504.AL = ait504.isLow
        HMI.AIT504.ALL = ait504.isLowLow

        # HMI.PIT501.Pv = pit501.value
        # HMI.PIT501.AHH = pit501.isHighHigh
        # HMI.PIT501.AH = pit501.isHigh
        # HMI.PIT501.AL = pit501.isLow
        # HMI.PIT501.ALL = pit501.isLowLow
        #
        # HMI.PIT502.Pv = pit502.value
        # HMI.PIT502.AHH = pit502.isHighHigh
        # HMI.PIT502.AH = pit502.isHigh
        # HMI.PIT502.AL = pit502.isLow
        # HMI.PIT502.ALL = pit502.isLowLow
        #
        # HMI.PIT503.Pv = pit503.value
        # HMI.PIT503.AHH = pit503.isHighHigh
        # HMI.PIT503.AH = pit503.isHigh
        # HMI.PIT503.AL = pit503.isLow
        # HMI.PIT503.ALL = pit503.isLowLow

        HMI.P501.Status = p501.value
        HMI.P502.Status = p502.value
        HMI.MV501.Status=mv501.value
        HMI.MV502.Status = mv502.value
        HMI.MV503.Status = mv503.value
        HMI.MV504.Status = mv504.value

        HMI.P6.state = p6.state
        # HMI.FIT601.Pv = fit601.value
        # HMI.FIT601.AHH = fit601.isHighHigh
        # HMI.FIT601.AH = fit601.isHigh
        # HMI.FIT601.AL = fit601.isLow
        # HMI.FIT601.ALL = fit601.isLowLow
        HMI.P601.Status = p601.value
        HMI.P602.Status = p602.value
        HMI.P603.Status = p603.value

        PLC1.Pre_Main_Raw_Water(IO_DI_WIFI, IO_P1, HMI, Sec_P, Min_P)
        PLC2.Pre_Main_UF_Feed_Dosing(IO_DI_WIFI,IO_P2,HMI,Sec_P,Min_P)
        PLC3.Pre_Main_UF_Feed(IO_DI_WIFI,IO_P3,HMI,Sec_P,Min_P)
        PLC4.Pre_Main_RO_Feed_Dosing(IO_DI_WIFI,IO_P4,HMI,Sec_P,Min_P)
        PLC5.Pre_Main_High_Pressure_RO(IO_DI_WIFI,IO_P5,HMI,Sec_P,Min_P)
        PLC6.Pre_Main_Product(IO_DI_WIFI,IO_P6,HMI,Sec_P,Min_P)
        DO_all=plc_simulation.print_all_output(IO_P1,IO_P2,IO_P3,IO_P4,IO_P5,IO_P6)
        DO_plc1=DO_all[0]
        DO_plc2=DO_all[1]
        print (DO_plc1)
        print (DO_plc2)
        # data = {
        #     "PLC1": {
        #         "P1.MV101.DO_Open":DO_plc1[0],
        #         "P1.MV101.DO_Close": DO_plc1[1],
        #     "P1.P101.DO_Start":DO_plc1[2],
        #     "P1.P102.DO_Start": DO_plc1[3]},
        #
        #     "PLC2" : {
        #         "P2.MV201.DO_Open":DO_plc2[0],
        #         "P2.MV201.DO_Close":DO_plc2[1],
        #         "P2.P201.DO_Start":DO_plc2[2],
        #         "P2.P202.DO_Start":DO_plc2[3],
        #         "P2.P203.DO_Start":DO_plc2[4],
        #          "P2.P204.DO_Start":DO_plc2[5],
        #         "P2.P205.DO_Start":DO_plc2[6],
        #         "P2.P206.DO_Start":DO_plc2[7]
        #     }
        #
        # }
        # oa.publish_prediction(
        #     timestamp,
        #     data
        # )

    time.sleep(1)