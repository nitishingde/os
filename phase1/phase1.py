import math
fp = open('input.txt','r')
ff = iter(fp.read().split('\n'))
fp.close()
op = open('op.txt','w')


class phase1:

	JOB_ID, TTL, TLL = '','',''

	#Variable declaration
	#Memory
	M = ['    ' for i in range(100)]
	#Register
	R = [' ' for i in range(4)]
	#Instruction Register
	IR = [' ' for i in range(4)]
	#Instruction Counter
	IC = 0
	#Toggle
	C = False
	#Buffer
	buf =[' ' for i in range(40)]

	def flush(self):
		#Variable declaration
		#Memory00
		self.M = ['    ' for i in range(100)]
		#Register
		self.R = [' ' for i in range(4)]
		#Instruction Register
		self.IR = [' ' for i in range(4)]
		#Instruction Counter
		self.IC = 0#[' ' for i in range(2)]
		#Toggle
		self.C = False
		#Buffer
		self.buf =[' ' for i in range(40)]		

	def get_job_details(self):
		self.JOB_ID = self.buf[4:8]
		self.TTL = self.buf[8:12]
		self.TLL = self.buf[12:]
	
	def disp_job_details(self):
		print("JOB ID : {}\nTTL    : {}\nTLL    : {}".format(self.JOB_ID,self.TTL,self.TLL))
	
	def setm(self,m,strng):
		self.M[m] = strng

	def read(self,line):
		self.buf = line[:40]
		self.buf.strip('\n')		
		line = line[40:]
		return line

	def dispm(self,m):
		for i in range(int(m/4)):
			for j in range(4):
				print ("M[{:>2}] : {}".format(4*i+j,self.M[4*i+j]),"  ",end="")
			print()
		print()

	def MOS(self):
		self.IC = 0
		self.EXECUTE_USER_PROGRAM_SLAVE_MODE()

	def EXECUTE_USER_PROGRAM_SLAVE_MODE(self):
		while True:
			self.IR = self.M[self.IC]			
			#print ("{}) IR : {}".format(self.IC,self.IR[:2]))
			if self.IR[:2] == "LR":
				self.R = self.M[int(self.IR[2:])]

			elif self.IR[:2] == "SR":
				self.M[int(self.IR[2:])] = self.R
			
			elif self.IR[:2] == "CR":
				self.C = True if self.R == self.M[int(self.IR[2:])] else False
			
			elif self.IR[:2] == "BT":				
				self.IC = int(self.IR[2:]) if self.C == True else self.IC

			elif self.IR[:2] == "GD":
				self.MOS_MASTER_MODE(1)

			elif self.IR[:2] == "PD":				
				self.MOS_MASTER_MODE(2)

			elif 'H' in self.IR:
				self.MOS_MASTER_MODE(3)
				break

			self.IC = self.IC + 1			

	def MOS_MASTER_MODE(self,SI):
		if SI == 1:
			self.READ()
		elif SI == 2:
			self.WRITE()
		elif SI == 3:
			self.TERMINATE()

	def READ(self):
		#self.IR[3] = '0'
		self.buf = next(ff)
		self.buf = self.buf[:40]
		for i in range(0,40-len(self.buf)):
			self.buf = self.buf + ' '
		#print (self.IR[2:3])
		m = int(self.IR[2:3])*10
		#print (m)
		for i in range(0,10):
			self.M[m + i] = self.buf[4*i : 4*i + 4]


	def WRITE(self):
		#self.IR[4] = 0
		indx = int(self.IR[2:3])*10		
		#with open("op.txt","a") as op:
		for i in range(10):
			#print("to write {}".format(self.M[indx]))			
			op.write(self.M[indx+i])
		op.write('\n')

	def TERMINATE(self):
		#with open("op.txt","a") as op:
		op.write('\n\n')

	def LOAD(self):
		m = 0
		prgm = False
		self.flush()		
		for line in ff:
			while len(line) != 0:
				line = self.read(line)		
				#print (self.buf)
				if self.buf.startswith("$AMJ"):
					self.get_job_details()
					self.disp_job_details()					
					m = 0
					prgm = True
					continue

				elif self.buf.startswith("$DTA"):
					self.dispm(100)
					prgm = False					
					self.MOS()
					print("Memory After Execution :")
					self.dispm(100)
					print()

				elif self.buf.startswith("$END"):					
					self.flush()
					m = 0
						
				if prgm:
					if m == 100:
						break
					print("Program to be loaded : ",end="")

					while True:
						i = 0
						print(self.buf,end="")
						while i < len(self.buf):
							if i < len(self.buf) and m <= 100:
								if 'H' in self.buf[i:i+4]:
									self.setm(m,"H   ")
									i = i - 3
								else:
									self.setm(m,self.buf[i:i+4])
								#self.dispm(m)								
							
							else:
								self.setm(m,"    ")
							m = m + 1
							i = i + 4

						if len(line) == 0:
							print()
							self.dispm(m)
							break

						line = self.read(line)


if __name__ == '__main__':
	ph = phase1()
	ph.LOAD()
	op.close()
else:
	print('{} imported as module'.format(__name__))
