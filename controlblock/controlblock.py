from logicblock.logicblock import ALM
from logicblock.logicblock import SCL
from logicblock.logicblock import TONR
from logicblock.logicblock import bit_2_signed_integer
from logicblock.logicblock import signed_integer_2_bit
# 8 Classes in this file
class AIN_FBD:

	def __init__(self,L_Raw_RIO, H_Raw_RIO, L_Raw_WRIO, H_Raw_WRIO,HEU,LEU,HMI):
		self.L_Raw_RIO = L_Raw_RIO
		self.H_Raw_RIO = H_Raw_RIO
		self.L_Raw_WRIO= L_Raw_WRIO
		self.H_Raw_WRIO= H_Raw_WRIO
		self.HEU       = HEU
		self.LEU       = LEU

		self.Hty = HMI.Hty
		self.Wifi_Enb = HMI.Wifi_Enb
		self.AHH = HMI.AHH
		self.AH = HMI.AH
		self.AL = HMI.AL
		self.ALL = HMI.ALL
	def AIN_FBD(self,WRIO_Enb,IO,HMI):
		Raw_RIO = IO.AI_Value
		Raw_WRIO = IO.W_AI_Value
		RIO_Hty = IO.AI_Hty
		WRIO_Hty = IO.W_AI_Hty 

		SAHH = HMI.SAHH
		SAH  = HMI.SAHH
		SAL  = HMI.SAL
		SALL = HMI.SALL
		Simulation = HMI.Sim
		#print (WRIO_Enb,self.H_Raw_RIO,self.L_Raw_RIO)
		if WRIO_Enb:
			self.Wifi_Enb	 =  1
			Mid_Raw		 =  Raw_WRIO
			Mid_H_Raw	 =  self.H_Raw_WRIO
			Mid_L_Raw	 =  self.L_Raw_WRIO
			Mid_Inst_Hty 	 =  WRIO_Hty
		else:
			self.Wifi_Enb	 =  0
			Mid_Raw		 =  Raw_RIO
			Mid_H_Raw	 =  self.H_Raw_RIO
			Mid_L_Raw	 =  self.L_Raw_RIO
			Mid_Inst_Hty 	 =  RIO_Hty


		#Calculation for PV*)
		if Simulation:
			HMI.Pv		 = HMI.Sim_Pv 
		else:
			#print (Mid_Raw, Mid_H_Raw,Mid_L_Raw, self.HEU, self.LEU)
			SCALE_Out = SCL(Mid_Raw, Mid_H_Raw,Mid_L_Raw, self.HEU, self.LEU)

			if SCALE_Out<0:
				HMI.Pv	 =  0
			else: 
				HMI.Pv	 = SCALE_Out
			HMI.Sim_PV	 = HMI.Pv



		#Alarms*)
		self.AHH, self.AH, self.AL, self.ALL = ALM(HMI.Pv,SAHH,SAH,SAL,SALL)

		self.Hty =  Mid_Inst_Hty and (Mid_Raw  >  Mid_L_Raw) and (Mid_Raw < Mid_H_Raw)
		HMI.Hty = self.Hty
		HMI.Wifi_Enb = self.Wifi_Enb
		HMI.AHH = self.AHH
		HMI.AH  = self.AH
		HMI.AL  = self.AL
		HMI.ALL = self.ALL

			
class MV_FBD:
	def __init__(self, Open_TM, Close_TM,HMI):
		self.TON_Close = TONR(Close_TM)
		self.TON_Open  = TONR(Open_TM)
		self.FTO = HMI.FTO
		self.FTC = HMI.FTC
		self.Cmd_Open = HMI.Open
		self.Cmd_Close = HMI.Close

	def MV_FBD(self, AutoInp,IO,HMI):
		ZSO = IO.DI_ZSO
		ZSC = IO.DI_ZSC
		Auto = HMI.Auto
		self.TON_Close.TONR(self.Cmd_Close)
		self.TON_Open.TONR(self.Cmd_Open)
		if ZSC:
			HMI.Status = 1
		elif ZSO:
			HMI.Status = 2
		else:
			HMI.Status = 70
		# transfer
		HMI.Avl = Auto and not self.FTC and not self.FTO
		if HMI.Reset:
			self.FTC = 0
			self.FTO = 0
		if not Auto:
			if HMI.Cmd == 1:
				self.Cmd_Close = 1
				self.Cmd_Open  = 0
				if self.TON_Close.DN and not ZSC:
					self.FTC = 1
					self.FTO = 0
			elif HMI.Cmd == 2:
				if self.FTO or self.FTC:
					self.Cmd_Close = 0
					self.Cmd_Open = 1
				if self.TON_Open.DN and not ZSC:
					self.FTC = 0
					self.FTO = 1
					HMI.Cmd = 1
			else:
				print ("Error, Cmd value must be 1 or 2")
		else:
			if ZSO:
				Cmd = 2
			if ZSC:
				Cmd = 1
			if AutoInp and (not self.FTC and not self.FTO):
				self.Cmd_Close = 0
				self.Cmd_Open  = 1
				if self.TON_Open.DN and not ZSC:
					self.FTC = 0
					self.FTO = 1
			else:
				self.Cmd_Close = 1
				self.Cmd_Open  = 0
				if self.TON_Close.DN and not ZSC:
					self.FTC = 1
					self.FTO = 0	
		IO.DO_Open = self.Cmd_Open
		IO.DO_Close= self.Cmd_Close
		HMI.FTO = self.FTO
		HMI.FTC = self.FTC

class FIT_FBD:
	def __init__(self,L_Raw_RIO, H_Raw_RIO, L_Raw_WRIO, H_Raw_WRIO,HEU,LEU,HMI):
		self.Hty = HMI.Hty
		self.Wifi_Enb = HMI.Wifi_Enb
		self.AHH = HMI.AHH
		self.AH = HMI.AH
		self.AL = HMI.AL
		self.ALL = HMI.ALL
		self.L_Raw_RIO = L_Raw_RIO
		self.H_Raw_RIO = H_Raw_RIO
		self.L_Raw_WRIO = L_Raw_WRIO
		self.H_Raw_WRIO = H_Raw_WRIO
		self.HEU = HEU
		self.LEU = LEU
	def FIT_FBD(self, WRIO_Enb, Totaliser_Enb, IO,HMI,Sec_P):
		Raw_RIO = IO.AI_Value
		Raw_WRIO = IO.W_AI_Value
		RIO_Hty = IO.AI_Hty
		WRIO_Hty = IO.W_AI_Hty 

		SAHH = HMI.SAHH
		SAH  = HMI.SAH
		SAL  = HMI.SAL
		SALL = HMI.SALL
		Simulation = HMI.Sim
		Rst_Totaliser = HMI.Rst_Totaliser

		if WRIO_Enb:
			self.Wifi_Enb = 1
			Mid_Raw = Raw_WRIO
			Mid_H_Raw = self.H_Raw_WRIO
			Mid_L_Raw = self.L_Raw_WRIO
			Mid_Inst_Hty = WRIO_Hty
		else:
			self.Wifi_Enb = 0
			Mid_Raw = Raw_RIO
			Mid_H_Raw = self.H_Raw_RIO
			Mid_L_Raw = self.L_Raw_RIO
			Mid_Inst_Hty = RIO_Hty
		if Simulation:
		   	HMI.Pv = HMI.Sim_PV
		else:
			Scale_Out = SCL( Mid_Raw, Mid_H_Raw, Mid_L_Raw, self.HEU, self.LEU)
			if Scale_Out > 0:
				HMI.Pv = Scale_Out
			elif Scale_Out <= 0:
				HMI.Pv = 0.0
			HMI.Sim_Pv = HMI.Pv
		self.AHH, self.AH, self.AL, self.ALL = ALM(HMI.Pv, SAHH, SAH, SAL, SALL)
		if Totaliser_Enb:
			if Sec_P:
				HMI.Totaliser = HMI.Totaliser + abs(HMI.Pv)/3600
		if Rst_Totaliser:
			HMI.Totaliser = 0
		self.Hty = Mid_Inst_Hty and (Mid_Raw > Mid_L_Raw) and (Mid_Raw > Mid_H_Raw) 
		
		HMI.Hty = self.Hty
		HMI.Wifi_Enb = self.Wifi_Enb
		HMI.AHH = self.AHH
		HMI.AH  = self.AH
		HMI.AL  = self.AL
		HMI.ALL = self.AHH

class PMP_FBD:
	def __init__(self,Start_TM, Stop_TM,HMI):
		self.TON_Stop = TONR(Stop_TM)
		self.TON_Start  = TONR(Start_TM)
		self.Cmd_Start = 0
		self.Avl = HMI.Avl
		self.Fault = HMI.Fault
		self.FT_Stop = HMI.FTS
		self.FT_Start = HMI.FTR
		self.RunHr = HMI.RunHr
		self.Total_RunHr = HMI.RunHr
		self.SD = bit_2_signed_integer(HMI.Shutdown)
		self.Fault = 0
		self.RunMin = 0
		self.Total_RunMin = 0
	def PMP_FBD(self, AutoInp,IO, HMI, Min_P):
		Auto = HMI.Auto
		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Trip   = IO.DI_Fault
	
		Rst = HMI.Reset
		Rst_RunHr = HMI.Reset_RunHr
		Permissive = bit_2_signed_integer(HMI.Permissive)
		self.a = Permissive
		Shutdown   = bit_2_signed_integer(HMI.SD)

		self.TON_Stop.TONR(not self.Cmd_Start)
		self.TON_Start.TONR(self.Cmd_Start)
		if not Run:
			HMI.Status = 1
		else:
			HMI.Status = 2
		if self.Fault:
			HMI.Fault = 1
		else:
			HMI.Fault = 0
		if HMI.Reset:
			if not self.TON_Start.DN:
				self.FT_Stop = 0
			if not self.TON_Stop.DN:
				self.FT_Start = 0
			self.SD = 0
		self.Fault = Trip or self.SD != 0
		HMI.Remote = Remote
		self.Avl = Auto and Remote and not self.Fault and not self.FT_Start and not self.FT_Stop and self.SD == 0
		if Remote:
			if not Auto:
				if HMI.Cmd == 1:
					self.Cmd_Start = 0
					if self.TON_Stop.DN and Run:
						self.FT_Start = 0
						self.FT_Stop  = 1
				if HMI.Cmd == 2:
					if not self.Fault and not self.FT_Start and not self.FT_Stop and Permissive == -1 and bit_2_signed_integer(HMI.SD) == 0:
						self.Cmd_Start = 1
					elif self.Cmd_Start and bit_2_signed_integer(HMI.SD) != 0 or self.Fault:
						self.SD = bit_2_signed_integer(HMI.SD)
						self.Cmd_Start = 0
						HMI.Cmd = 1
					elif Permissive != -1:
						HMI.Cmd = 1
					if self.TON_Start.DN and not Run:
						self.FT_Start = 1
						self.FT_Stop  = 0
						self.Cmd_Start = 0
						HMI.Cmd = 1
			else:
				if Run:
					self.Cmd = 2
				if not Run or self.Fault or self.FT_Start or self.FT_Stop:
					self.Cmd = 1
				if AutoInp:
					if not self.Fault and not self.FT_Start and not self.FT_Stop and Permissive == -1 and bit_2_signed_integer(HMI.SD)== 0:
						self.Cmd_Start = 1
					elif self.Cmd_Start or bit_2_signed_integer(HMI.SD) != 0 or self.Fault:
						self.SD = bit_2_signed_integer(HMI.SD)
						self.Cmd_Start = 0
					if self.TON_Start.DN and not Run:
						self.FT_Start = 1
						self.FT_Stop  = 0
						self.Cmd_Start = 0
						HMI.Cmd = 1
				else:
					self.Cmd_Start = 0
					if self.TON_Stop.DN and Run:
						self.FT_Start = 0	
						self.FT_Stop  = 1
		else:
			self.Cmd_Start = 0
			self.Cmd = 1
			self.FT_Start = 0
			self.FT_Stop  = 0
		if Run:
			if Min_P:
				self.RunMin = self.RunMin + 1.0
				self.Total_RunMin = self.Total_RunMin + 1.0
		self.RunHr = self.RunMin/60.0
		self.Total_RunHr = self.Total_RunMin/60.0
		if Rst_RunHr:
			self.RunMin = 0
		
		HMI.Avl = self.Avl
		HMI.Fault = self.Fault
		HMI.FTS = self.FT_Stop
		HMI.FTR = self.FT_Start
		HMI.RunHr = self.RunHr
		HMI.Total_RunHr = self.Total_RunHr
		HMI.Shutdown = signed_integer_2_bit(self.SD)
	
		IO.DO_Start = self.Cmd_Start
	

class Duty2_FBD:
	def __init__(self):
		self.Start_Pmp1 = 0
		self.Start_Pmp2 = 0
	def Duty2_FBD(self, AutoInp, PMP1,PMP2,HMI): #PMP1 and PMP2 should be the class of pump1 and pump2 	
		Selection = HMI.Selection

		if PMP1.Status == 2 or PMP2.Status ==2:
			HMI.Pump_Running = 1
		else:
			HMI.Pump_Running =0
		HMI.Both_Pmp_Not_Avl = not PMP1.Avl and not PMP2.Avl
		if AutoInp:
			if Selection == 1:
				if PMP1.Avl:
					self.Start_Pmp1 = 1
					self.Start_Pmp2 = 0
					HMI.Selected_Pmp_Not_Avl = 0
				elif not PMP1.Avl and PMP2.Avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 1
					HMI.Selected_Pmp_Not_Avl = 1
				elif not PMP1.Avl and not PMP2.Avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 0
				else:
					HMI.Selected_Pmp_Not_Avl = 0
			if Selection == 2:
				if PMP2.Avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 1
					HMI.Selected_Pmp_Not_Avl = 0
				elif not PMP1.Avl and PMP2.Avl:
					self.Start_Pmp1 = 1
					self.Start_Pmp2 = 0
					HMI.Selected_Pmp_Not_Avl = 1
				elif not PMP1.Avl and not PMP2.Avl:
					self.Start_Pmp1 = 0
					self.Start_Pmp2 = 0
				else:
					HMI.Selected_Pmp_Not_Avl = 0
		else:
			self.Start_Pmp1 = 0
			self.Start_Pmp2 = 0

class SWITCH_FBD:
	def __init__(self,HMI):
		Delay = HMI.Delay
		self.TON_Delay = TONR(Delay)
	def SWITCH_FBD(self, IO,HMI):
		Alarm = IO.DI_LS	
		self.TON_Delay.TONR(Alarm)
		HMI.Status = self.TON_Delay.DN
		self.Status = self.TON_Delay.DN
		

class UV_FBD:
	def __init__(self, Start_TM, Stop_TM,HMI):
		self.TON_Stop   = TONR(Stop_TM)
		self.TON_Start  = TONR(Start_TM)
		self.Cmd_Start  = 0
		self.Fault = 0
		self.Avl = HMI.Avl
		self.FT_Stop = HMI.FTS
		self.FT_STart = HMI.FTR
		self.RunHr = HMI.RunHr
		self.Total_RunHr = HMI.RunHr
		self.SD = bit_2_signed_integer(HMI.Shutdown)

	def UV_FBD(self, AutoInp,IO, HMI):
		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Trip   = IO.DI_Fault

		Auto = HMI.Auto
		Rst  = HMI.Reset
		Rst_RunHr = HMI.Reset_RunHr
		Permissive = bit_2_signed_integer(HMI.Permissive)
		Shutdown = bit_2_signed_integer(HMI.SD)

		self.TON_Stop.TONR(not self.Cmd_Start)
		self.TON_Start.TONR(self.Cmd_Start) 
		self.FT_Start = HMI.FTR
		self.FT_Stop  = HMI.FTS
		if not Run:
			HMI.Status = 1
		else:
			HMI.Status = 2
		if self.Fault:
			HMI.Fault = 1
		else:
			HMI.Fault = 0
		if HMI.Reset:
			if not self.TON_Stop.DN:
				self.FT_Stop = 0
			if not self.TON_Start.DN:
				self.FT_STart = 0
			self.SD = 0
		self.Fault = Trip
		HMI.Remote = Remote
		self.Avl = Auto and Remote and not self.Fault and not self.FT_Start and not self.FT_Stop and self.SD == 0
		if Remote:
			if not Auto:
				if HMI.Cmd == 1:
					self.Cmd_Start = 0
					if self.TON_Stop.DN and Run:
						self.FT_Start = 0
						self.FT_Stop  = 1
				if HMI.Cmd == 2:
					if not self.Fault and not self.FT_Start and not self.FT_Stop and Permissive == -1 and bit_2_signed_integer(HMI.SD) == 0:
						self.Cmd_Start = 1
					elif self.Cmd_Start and bit_2_signed_integer(HMI.SD) != 0 or self.Fault:
						self.SD = bit_2_signed_integer(HMI.SD)
						self.Cmd_Start = 0
						HMI.Cmd = 1
					if self.TON_Start.DN and not Run:
						self.FT_Start = 1
						self.FT_Stop  = 0
						self.Cmd_Start = 0
						HMI.Cmd  = 1
			else:
				if Run:
					self.Cmd = 2
				if not Run or self.Fault or self.FT_Start or self.FT_Stop:
					self.Cmd = 1
				if AutoInp:
					if not self.Fault and not self.FT_Start and not self.FT_Stop and Permissive == -1 and bit_2_signed_integer(HMI.SD) == 0:
						self.Cmd_Start = 1
					elif self.Cmd_Start or bit_2_signed_integer(HMI.SD) != 70 or self.Fault:
						self.SD = bit_2_signed_integer(HMI.SD)
						self.Cmd_Start = 0
					if self.TON_Start.DN and not Run:
						self.FT_Start = 1
						self.FT_Stop  = 0
						self.Cmd_Start = 0
						HMI.Cmd = 1
				else:
					self.Cmd_Start = 0
					if self.TON_Stop.DN and Run:
						self.FT_Start = 0
						self.FT_Stop  = 1
		else:
			self.Cmd_Start = 0
			self.Cmd = 1	
			self.FT_Start = 0
			self.FT_STart = 0
		
		HMI.Avl = self.Avl
		HMI.Fault = self.Fault
		HMI.FTS = self.FT_Stop
		HMI.FTR = self.FT_Start
		HMI.RunHr = self.RunHr
		HMI.Total_RunHr = self.Total_RunHr
		HMI.Shutdown = signed_integer_2_bit(self.SD)
		IO.Start = self.Cmd_Start	

class VSD_FBD:
	def __init__(self,Start_TM, Stop_TM, HMI):
		self.TON_Start = TONR(Start_TM)
		self.TON_Stop  = TONR(Stop_TM)
		self.Fault = HMI.Fault
		self.FT_Start = HMI.FTR
		self.FT_Stop = HMI.FTS
		self.SD = bit_2_signed_integer(HMI.Shutdown)
		self.RunMin = 0
		self.Total_RunMin = 0
		self.Speed = HMI.Speed
		self.Rdy = HMI.Drive_Ready
		

	def VSD_FBD(self, AutoInp, AutoSpeed, VSD_In, VSD_Out,IO, HMI, Min_P ):
		Remote = IO.DI_Auto
		Run    = IO.DI_Run
		Start_PB = IO.DI_VSD_PB

		Trip = VSD_In.Faulted

		Auto = HMI.Auto
		Rst  = HMI.Reset
		Rst_RunHr = HMI.Reset_RunHr
		Speed_Cmd = HMI.Speed_Command
		Permissive = bit_2_signed_integer(HMI.Permissive)
		Shutdown = bit_2_signed_integer(HMI.SD)
		
		self.TON_Start.TONR(VSD_Out.Start)
		self.TON_Stop.TONR(VSD_Out.Stop)
		if not VSD_In.Active:
			HMI.Status = 1
		else:
			HMI.Status = 2
		self.Rdy = VSD_In.Ready
		self.Speed = VSD_In.OutputFreq
		HMI.Remote = Remote
		self.Avl = Auto and Remote and not self.Fault and not self.FT_Start and not self.FT_Stop and self.SD == 0
		HMI.Fault = VSD_In.Faulted or Trip or self.SD
		if HMI.Reset:
			VSD_Out.ClearFaults = 1
			HMI.Shutdown = [0] * 32	# In original PLC code, here it's HMI.SHUTDOWN,  we doubt it's global HMI's SHUTDOWN variable, or it's not case sensitive and equal to Shutdown like we treat it here.
			if not self.TON_Stop.DN:
				self.FT_Stop = 0
			if not self.TON_Start.DN:
				self.FT_Start = 0
			self.SD = 0
		if Remote:
			if not Auto:
				if HMI.Cmd == 1:
					VSD_Out.Start = 0 
					VSD_Out.Stop  = 1
					VSD_Out.FreqCommand = Speed_Cmd
					if self.TON_Stop.DN and VSD_In.Active:
						self.FT_Start = 0
						self.FT_Stop  = 1
				if HMI.Cmd == 2:
					if not VSD_In.Faulted and (not self.FT_STart or self.FT_Stop) and Permissive == -1 and bit_2_signed_integer(HMI.SD) == 0:
						VSD_Out.Start = 1
						VSD_Out.Stop  = 0
						VSD_Out.FreqCommand = Speed_Cmd * 100
				elif VSD_Out.Start or (bit_2_signed_integer(HMI.SD) != 0) or self.Fault:
					self.SD = bit_2_signed_integer(HMI.SD)
					VSD_Out.Start = 0
					VSD_Out.Stop  = 1
					VSD_Out.FreqCommand = Speed_Cmd * 100
					HMI.Cmd = 1
				if self.TON_Start.DN and not Run:
					self.FT_Start = 1
					self.FT_Stop  = 0
					self.VSD_Out.Start = 0
					self.VSD_Out.Stop  = 1
					HMI.Cmd = 1
			else:
				if VSD_In.Active:
					HMI.Cmd = 2 # Cmd or HMI.Cmd, the original code is realy ambiguous 
				if not VSD_In.Active or VSD_In.Faulted or self.FT_Start or self.FT_Stop:
					HMI.Cmd = 1
				if AutoInp:
					if not VSD_In.Faulted and (not self.FT_Start or self.FT_Stop) and Permissive == -1 and bit_2_signed_integer(HMI.SD) == 0:
						VSD_Out.Start = 1
						VSD_Out.Stop  = 0
						VSD_Out.FreqCommand = AutoSpeed * 100
					elif VSD_Out.Start or bit_2_signed_integer(HMI.SD) != 0 or self.Fault:
						self.SD = bit_2_signed_integer(HMI.SD)
						VSD_Out.Start = 0
						VSD_Out.Stop = 0
						HMI.Cmd = 1
					if self.TON_Start.DN and not VSD_In.ACtive:
						VSD_Out.Start = 0
						VSD_Out.Stop  = 1
						VSD_Out.FreqCommand = AutoSpeed * 100
						HMI.Cmd = 1
				else:
					VSD_Out.Start = 0
					VSD_Out.Stop  = 1
					if self.TON_Stop.DN and VSD_In.Active:
						self.FT_Start = 0
						self.FT_Stop = 1
		else:
			if Start_PB:
				VSD_Out.Start = 1
				VSD_Out.Stop  = 0
				VSD_Out.FreqCommand = Speed_Cmd * 110
			else:
				VSD_Out.Start = 0
				VSD_Out.Stop = 1
				VSD_Out.FreqCommand = Speed_Cmd * 110
			if Run:
				HMI.Cmd = 2
			if not Run or self.Fault or self.FT_Start or self.FT_Stop:
				HMI.Cmd = 1
		if Run or VSD_In.Active:
			if Min_P:
				self.RunMin += 1
				self.Total_RunMin += 1
		self.RunHr = self.RunMin / 60.0
		self.Total_RunHr = self.Total_RunMin / 60.0
		if Rst_RunHr:
			self.RunMin = 0
				

		HMI.Avl = self.Avl
		HMI.Fault = self.Fault
		HMI.FTS = self.FT_Stop
		HMI.FTR = self.FT_Start
		HMI.RunHr = self.RunHr
		HMI.Total_RunHr = self.Total_RunHr
		HMI.Speed = self.Speed
		HMI.Drive_Ready = self.Rdy
		HMI.Shutdown = signed_integer_2_bit(self.SD)
