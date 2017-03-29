import random
#from phase1.phase1 import phase1
from phase1.os_packages.PCB import PCB

class phase2():

	#initialization
	def __init__(self):
		#Memory
		self.M = ['    ' for i in range(300)]
		#Register
		self.R = [' ' for i in range(4)]
		#Instruction Register
		self.IR = [' ' for i in range(4)]
		#Instruction Counter
		self.IC = 0
		#Toggle
		self.C = False
		#Buffer
		self.buffer =[' ' for i in range(40)]
		#Page Table Register
		self.PTR = -1
		#Addresses
		self.RA = 0
		#Memory Check Counter
		self.is_empty = [True for i in range(30)]
		#Interrupts
		self.SI, self.PI, self.TI = 0, 0, 0
		#Buffer
		self.buffer =[' ' for i in range(40)]
		#PCB
		self.pcb = PCB()

	#reset parameters
	def flush(self):
		self.__init__()

	#paging
	def INITIALIZE_PAGE_TABLE(self):
		self.PTR = 10*random.randint(0,29)
		self.is_empty[int(self.PTR/10)] = False
		for i in range(self.PTR,self.PTR+10):
			self.M[i] = '0 **'

	def ALLOCATE(self,addr):
		while True:
			m = random.randint(0,29)
			if self.is_empty[m]==True:
				self.is_empty[m] = False
				self.M[addr] = '1 ' + str(m) if m >= 10 else '1 0' + str(m)
				return 10*m

	def ADDRESS_MAP(self,VA):

		if VA.isdigit():
			add = int(self.PTR + int(VA)/10);
			if self.M[add] == '0 **':
				self.PI = 3
				self.SI = 0
			else:
				#print ("DBG {}".format(add,self.M[add][2:]))
				#self.dispm(300)
				if self.M[add][2:].isdigit():
					self.RA = int(self.M[add][2:])*10 + int(VA)%10
				else:
					self.PI = 2
				#print("RA :{}\n".format(self.RA))
		else:
			if 'H' in self.IR:
				self.SI = 3
			else:
				self.PI = 2

	#buffer
	#loads buffer(40B) and returns the remaining line
	def load_buffer(self,line):
		self.buffer = line[:40]
		self.buffer.strip('\n')
		line = line[40:]
		return line

	def setm(self,m,strng):
		self.M[m] = strng

	def dispm(self,m):
		for i in range(int(m/4)):
			for j in range(4):
				print ("M[{:>3}] : {}".format(4*i+j,self.M[4*i+j]),"  ",end="")
			print()
		print()

	def read(self,line):
		self.buffer = line[:40]
		self.buffer.strip('\n')
		line = line[40:]
		return line
		
	#execution
	def MOS(self):

		if self.TI == 0:
			if self.SI > 0 and self.PI == 0:
				if self.SI == 1:
					self.READ()
				elif self.SI == 2:
					self.WRITE()
				elif self.SI == 3:
					self.TERMINATE(0)

			if self.PI > 0:
				if self.PI == 1:
					self.TERMINATE(4)
				elif self.PI == 2:
					self.TERMINATE(5)
				elif self.PI == 3:
					if self.SI == 1:#self.IR.find('GD') != -1 or self.IR.find('SR') != -1:
						self.RA = self.ALLOCATE( int(self.PTR + int(int(self.IR[2:])/10)) )
						self.IC = self.IC - 1
						self.SIMULATION()
					else:
						self.TERMINATE(6)
					self.PI = 0

		elif self.TI == 2:
			if self.SI > 0 and self.PI == 0:
				if self.SI == 1:
					self.TERMINATE(3)
				elif self.SI == 2:
					self.TERMINATE(3)
				elif self.SI == 3:
					self.TERMINATE(0)

			if self.PI > 0:

				if self.PI == 1:
					self.TERMINATE(4)
				elif self.PI == 2:
					self.TERMINATE(5)
				elif self.PI == 3:
					self.PI = 0
				self.TERMINATE(3)

		#self.SI, self.PI, self.TI = 0, 0, 0

	def READ(self):
		if '$END' in self.buffer:
			self.TERMINATE(1)
			self.TI = 2
			return
		self.buffer = next(ff)
		if '$END' in self.buffer:
			self.TERMINATE(1)
			self.TI = 2
			return
		#self.pcb.TTC = self.pcb.TTC + 2
		self.buffer = self.buffer[:40]
		for i in range(0,40-len(self.buffer)):
			self.buffer = self.buffer + ' '
		for i in range(0,10):
			self.M[self.RA + i] = self.buffer[4*i : 4*i + 4]
		#self.dispm(300)

	def WRITE(self):
		self.SIMULATION()
		self.pcb.TLC = self.pcb.TLC + 1
		if self.pcb.TLC <= self.pcb.TLL:
			#with open("op.txt","a") as op:
			for i in range(10):
				#print("to write {}".format(self.M[indx]))
				op.write(self.M[self.RA+i])
			op.write('\n')

		else:
			self.TERMINATE(2)

	def EXECUTE_USER_PROGRAM(self):
		self.SI, self.PI, self.TI = 0, 0, 0
		print("Instructions :")
		while True:
			#	break
			self.ADDRESS_MAP(str(self.IC))
			#print ("DBG2 {}".format(self.RA))
			self.IR = self.M[self.RA]
			self.IC = self.IC + 1

			self.ADDRESS_MAP(self.IR[2:])
			print("IR :{} : {}".format(self.IR,self.pcb.TTC))
			#print("RA :{}".format(self.RA))

			if self.IR[:2] == "LR":
				self.SIMULATION()
				if self.PI == 0 and self.TI == 0:
					#self.pcb.TTC = self.pcb.TTC + 1
					self.R = self.M[self.RA]
					#print ("Reg :{}".format(self.R))
				else:
					self.MOS()
					self.SI = self.PI = 0

			elif self.IR[:2] == "SR":
				if self.PI == 0 and self.TI == 0:
					self.SIMULATION()
					#self.pcb.TTC = self.pcb.TTC + 1
					self.M[self.RA] = self.R
					#print ("RA :{} MEM : {}".format(self.RA,self.M[self.RA]))
				else:
					self.SI = 1
					self.MOS()
					self.SI = self.PI = 0

			elif self.IR[:2] == "CR":
				self.SIMULATION()
				if self.PI == 0 and self.TI == 0:
					#self.pcb.TTC = self.pcb.TTC + 1
					#print("C before:{}".format(self.C))
					self.C = True if self.R == self.M[self.RA] else False
					#print("C before:{}".format(self.C))
				else:
					self.MOS()
					self.SI = self.PI = 0

			elif self.IR[:2] == "BT":
				self.SIMULATION()
				if self.PI == 0 and self.TI == 0:
					#self.pcb.TTC = self.pcb.TTC + 1
					#print ("BT before {}".format(self.IC))
					self.IC = int(self.IR[2:]) if self.C == True else self.IC
					#print ("BT after {}".format(self.IC))
				else:
					self.MOS()
					self.SI = self.PI = 0

			elif self.IR[:2] == "GD":
				#self.SIMULATION()
				if self.PI != 3:
					self.SIMULATION()
				self.SI = 1#if self.PI == 0 else 0
				self.MOS()
				self.SI = self.PI = 0


			elif self.IR[:2] == "PD":
				self.SI = 2#if self.PI == 0 else 0
				self.MOS()

			elif self.IR.find('H ') != -1:
				self.SIMULATION()
				self.SI = 3
				self.MOS()
				break

			else:
				self.PI = 1
				self.MOS()
				self.SI = self.PI = 0

			if self.TI == 2:
				break

		self.pcb.disp_limits()
		self.dispm(300)

	def SIMULATION(self):
		self.pcb.TTC = self.pcb.TTC + 1
		if self.pcb.TTC > self.pcb.TTL:
			self.TI = 2

	def START_EXECUTION(self):
		self.IC = 0
		self.EXECUTE_USER_PROGRAM()

	def TERMINATE(self, EM):

		if EM == 0:
			print ("No error.")
			op.write("No error.\n\n")

		elif EM == 1:
			print("Out of data.")
			op.write("Out of data.\n\n")

		elif EM == 2:
			print("Line limit exceeded.")
			op.write("Line limit exceeded.\n\n")

		elif EM == 3:
			print("Time limit exceeded.")
			op.write("Time limit exceeded.\n\n")

		elif EM == 4:
			print("Operation code error.")
			op.write("Operation code error.\n\n")

		elif EM == 5:
			print("Operand error.")
			op.write("Operand error.\n\n")

		elif EM == 6:
			print("Invalid page fault.")
			op.write("Invalid page fault.\n\n")

		op.write("IR : {}\nIC : {}\n".format(self.IR,self.IC))
		op.write( "JOB ID              : {}\nTotal Time Limit    : {}\nTotal Line Limit    : {}".format(self.pcb.JOB_ID,self.pcb.TTL,self.pcb.TLL))
		#op.write("\nTTC :{}\nTLC :{}\n".format(self.pcb.TTC,self.pcb.TLC))
		op.write("\n\nTime and Line counts :\nTTC :{}/{}\nTLC :{}/{}\n".format(self.pcb.TTC,self.pcb.TTL,self.pcb.TLC,self.pcb.TLL))
		op.write("--------------------------------------------------\n\n\n")

		self.TI = 2

	def LOAD(self):
		prgm = False
		self.flush()
		for line in ff:
			while len(line) != 0:
				#loads buffer(40B) and returns the remaining to the line
				line = self.load_buffer(line)
				#print (self.buffer)

				if self.buffer.startswith("$AMJ"):
					self.pcb.PCBin(self.buffer)
					self.pcb.disp_job_details()
					#print (self.buffer)
					self.INITIALIZE_PAGE_TABLE()
					print ("PTR :{}".format(self.PTR))
					prgm = True
					continue

				elif self.buffer.startswith("$DTA"):
					#self.dispm(300)
					print()
					prgm = False
					self.START_EXECUTION()
					#self.START_EXECUTION()
					#print("Memory After Execution :")
					#self.dispm(300)
					#print()

				if self.buffer.startswith("$END"):
					self.flush()
					print ("\n-------------------------------------------------------------\n")

				if prgm:
					#Program Card is Loaded
					print("Program to be loaded : ",end="")
					page = 0
					while True:
						i = 0
						print(self.buffer,end="")
						m = self.ALLOCATE(self.PTR + page)
						page = page + 1
						while i < len(self.buffer):
							if i < len(self.buffer):
								if 'H' in self.buffer[i:i+4]:
									self.setm(m,"H   ")
									i = i - 3
								else:
									self.setm(m,self.buffer[i:i+4])
								#self.dispm(m)

							else:
								self.setm(m,"    ")
							m = m + 1
							i = i + 4

						if len(line) == 0:
							print()
							#self.dispm(m)
							break

						line = self.read(line)


if __name__ == '__main__':
	fp = open('inp.txt','r')
	ff = iter(fp.read().split('\n'))
	fp.close()
	op = open('op.txt','w')
	ph = phase2()
	ph.LOAD()
	op.close()
else:
	print('{} imported as module'.format(__name__))
