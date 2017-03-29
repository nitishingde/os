class PCB:	
	
	def __init__(self):
		self.JOB_ID, self.TTL, self.TLL = -1, -1, -1
		self.TTC, self.TLC = 0, 0

	def PCBin(self, bu):
		buf = ''.join(bu)
		self.JOB_ID = int(buf[4:8])
		self.TTL = int(buf[8:12])
		self.TLL = int(buf[12:])
	
	def disp_job_details(self):
		print( "JOB ID              : {}\nTotal Time Limit    : {}\n\
Total Line Limit    : {}".format(self.JOB_ID,self.TTL,self.TLL))
		print("TTC :{}\nTLC :{}\n".format(self.TTC,self.TLC))

	def disp_limits(self):
		print("\nTime and Line counts :\nTTC :{}/{}\nTLC :{}/{}\n".format(self.TTC,self.TTL,self.TLC,self.TLL))

