class PCB:	
	
	def __init__(self):
		self.JOB_ID, self.TTL, self.TLL = -1, -1, -1
		self.TTC, self.LLC = 0, 0
		self.p_count, self.d_count, self.o_count = 0, 0, 0
		self.TS, self.TSC = 10, 0
		self.p_address, self.d_address, self.o_address = [ -1 for i in range(5)], [ -1 for i in range(5)], [ -1 for i in range(5)] 
		self.is_p, self.is_d = False, False
		self.PTR = -1
		#Register
		#self.R = [' ' for i in range(4)]
		#Instruction Register
		#self.IR = [' ' for i in range(4)]
		#Instruction Counter
		#self.IC = 0
		#Toggle
		#self.C = False

	def PCBin(self, bu):
		buf = ''.join(bu)
		self.JOB_ID = int(buf[4:8])
		self.TTL = int(buf[8:12])
		self.TLL = int(buf[12:])
		self.LLC = self.TTC = 0
		self.TSC = 2
		self.p_count = self.d_count = self.o_count = 0
	
	def disp_job_details(self):
		print( "JOB ID              : {}\nTotal Time Limit    : {}\n\
Total Line Limit    : {}".format(self.JOB_ID,self.TTL,self.TLL))
		print("TTC :{}\nLLC :{}\n".format(self.TTC,self.LLC))

	def disp_limits(self):
		print("\nTime and Line counts :\nTTC :{}/{}\nLLC :{}/{}\n".format(self.TTC,self.TTL,self.LLC,self.TLL))

