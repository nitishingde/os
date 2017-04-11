#from phase2.phase2 import phase2
import copy
import random
from phase2.phase1.os_packages.PCB import PCB
from collections import deque

dummy = True
fp = open('input.txt','r')
ff = iter(fp.read().split('\n'))
fp.close()

class phase3():
	
	def __init__(self):		
		#Memory
		self.M = ['    ' for i in range(300)]
		#Supervisory
		#self.S = [''.join(['*' for i in range(40)]) for i in range(10)]
		#Drum
		self.D = [''.join(['*' for i in range(40)]) for i in range(100)]
		#Paget Table Register
		self.PTR = -1
		#Memory Check Counter
		self.is_empty = [True for i in range(30)]
		#Register
		self.R = [' ' for i in range(4)]
		#Instruction Register
		self.IR = [' ' for i in range(4)]
		#Instruction Counter
		self.IC = 0
		#Toggle
		self.C = False
		#Buffer
		self.ebq, self.ifbq, self.ofbq = deque(str(i) for i in range(10)), deque(), deque() 
		#self.buffer =[' ' for i in range(40)]
		#PCB
		self.pcb, self.pcb_ld = PCB(), PCB()
		#PCB related Queues
		self.LQ, self.RQ, self.IOQ, self.TQ = deque(), deque(), deque(), deque()
		#Interrupts
		self.SI, self.PI, self.TI, self.IOI = 0, 0, 0, 0
		#Channel Timers
		self.CH1_timer, self.CH2_timer, self.CH3_timer = 0, 0, 0
		#Channel Flags
		self.CH1_flag, self.CH2_flag, self.CH3_flag = False, False, False
		#Card
		self.line = str()
		#Universal Timer
		self.UT = 0
		#Case Task
		self.case_task = '**'

	def dispm(self,m):
		for i in range(int(m/4)):
			for j in range(4):
				print ("M[{:>3}] : {}".format(4*i+j,self.M[4*i+j]),"  ",end="")
			print()
		print()
		       
	#paging
	def INITIALIZE_PAGE_TABLE(self):
		while True:
			PTR = 10*random.randint(0,29)
			if self.is_empty[int(PTR/10)] == True:
				break		
		
		self.is_empty[int(PTR/10)] = False
		
		for i in range(PTR,PTR+10):
			self.M[i] = '0 **'
		return PTR

	def ALLOCATE(self,addr):

		for i in range(addr,addr+10):
			if self.M[i] == '0 **':
				addr = i
				break

		while True:
			m = random.randint(0,29)
			if self.is_empty[m]==True:
				self.is_empty[m] = False
				self.M[addr] = str(self.LQ[0].JOB_ID) + ' ' + str(m) if m >= 10 else tr(self.LQ[0].JOB_ID)+' 0' + str(m)
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

	def start_CH1(self):
		self.CH1_timer = 0
		self.CH1_flag = True

	def start_CH2(self):
		self.CH2_timer = 0
		self.CH2_flag = True

	def start_CH3(self):
		self.CH3_timer = 0
		self.CH3_flag = True

	def SIMULATION(self):
		self.UT += 1

		if self.CH1_flag:
			self.CH1_timer +=  1
			if self.CH1_timer == 5:
				self.IOI =+ 1

		if self.CH2_flag:
			self.CH2_timer += 1
			if self.CH2_timer == 5:
				self.IOI =+ 2

		if self.CH3_flag:
			self.CH3_timer += 1
			#print("add3 {}".format(self.CH3_timer))
			if self.CH3_timer == 2:
				self.IOI += 4
				print(self.IOI)		
		
		print("UniversalTimer : {}".format(self.UT))
		print("*******************In Simulation*******************")		
		print("------------------------------")
		print("|       | CH-1 | CH-2 | CH-3 |")
		print("------------------------------")
		print("| Flags | {:.4} | {:.4} | {:.4} |".format(str(self.CH1_flag), str(self.CH2_flag), str(self.CH3_flag)))
		print("| Count | {:>4} | {:>4} | {:>4} |".format(self.CH1_timer,self.CH2_timer,self.CH3_timer))
		print("------------------------------")
		print("EBQ  		   :{}".format(self.ebq))
		print("IFBQ           :{}".format(self.ifbq))
				
		if self.IOI != 0 or self.SI != 0 or self.PI != 0 or self.TI != 0:
			print("IOI : {}".format(self.IOI))
			print('MOS Called')
			print()
			self.MOS()
		print()
		print("***************************************************")
		print()
		print()

	def MOS(self):		
		'''if self.SI > 0:
			if self.TI <= 1 and self.SI == 1:
				qwe
			if self.TI <= 1 and self.SI == 2:
				qwe
			if self.TI <= 1 and self.SI == 3:
				qwe
			if self.TI == 2 and self.SI == 1:
				qwe
			if self.TI == 2 and self.SI == 2:
				qwe
			if self.TI == 2 and self.SI == 3:
		'''
		if self.IOI == 1:
			self.IR1()

		elif self.IOI == 2:
			self.IR2()

		elif self.IOI == 3:
			self.IR2()
			self.IR1()

		elif self.IOI == 4:
			self.IR3()

		elif self.IOI == 5:
			self.IR1()
			self.IR3()

		elif self.IOI == 6:
			self.IR3()
			self.IR2()

		elif self.IOI == 7:
			self.IR2()
			self.IR1()
			self.IR3()

	def IR2(self):
		self.IOI -= 2

	def IR1(self):
		self.CH1_flag = False
		self.CH1_timer = 0
		eb = self.ebq.popleft()
		print("!--------------------IN IR1()--------------------!")	

		if ff != None:
			try:
        		# get the next item
				eb = next(ff)
				if( len(eb) < 40):
					eb += ''.join([' ' for i in range(40-len(eb))])
        		
        		# do something with element
			except StopIteration:
				#dummy = False
				#print(len(self.ebq))
				for i in range(100):
					if self.D[i][0] != '*':
						print (self.D[i])
				# if StopIteration is raised, break from loop
				#self.pcb.disp_job_details()
				#while len(self.LQ) != 0:
				#	p = self.LQ.popleft()
				#	p.disp_job_details()
				#print(len(self.LQ))
				#exit(0)
			#eb = next(ff)
			#print(eb)		
			self.ifbq.append(eb)
			print("Content of IFBQ : {}".format(self.ifbq))
			if ff != None and len(self.ebq) != 0:
				#print ('ir1')
				self.start_CH1()
			else:				
				#print(len(self.ebq))
				#print(len(self.ebq))
				for i in range(100):
					if self.D[i][0] != '*':
						print (self.D[i])
						print('here')

		self.IOI -= 1
		print("!----------------------IR1()---------------------!")	
		#print (self.IOI)
    
	def IR3(self):
		self.CH3_flag = False
		self.CH3_timer = 0
		print("!--------------------IN IR3()--------------------!")	
		
		if self.case_task == 'LD':
			#print("LLLLLLLLOOOO")
			_pcb = PCB()
			_pcb = copy.copy(self.LQ[0])
			self.case_task = ''
			if self.pcb_ld.PTR == -1:
				_pcb.PTR = self.INITIALIZE_PAGE_TABLE()
			print(_pcb.PTR)			
			#
			#_pcb.PTR = self.pcb_ld.PTR
			_pcb.disp_job_details()					
			buffer = ''
			for i in range(_pcb.p_count):					
				buffer += str(self.D[_pcb.p_address[i]])
			print(buffer)
			while len(buffer) != 0:
				m = self.ALLOCATE(_pcb.PTR)
				#page = page + 1				
				for m_addr in range(m,m+10):
					if 'H' not in buffer[:4]:
						self.M[m_addr] = buffer[:4]
						buffer = buffer[4:]
					else:
						self.M[m_addr] = 'H   '
						buffer = buffer[1:]					
				buffer = '' if buffer.strip() == '' else buffer
				self.dispm(300)
				print(buffer+'as')
			self.RQ.append(_pcb)
			self.LQ.popleft()

		if self.case_task == 'IS':
			print("Input Spooling")
			self.case_task == ''
			if len(self.ifbq[0]) != 0:
				ifb = self.ifbq.popleft()
				#.startswith('$AMJ')
				if ifb.startswith('$AMJ'):					
					self.pcb.is_p = True
					self.pcb.is_d = False
					self.pcb.PCBin(ifb)
					print("Updating pcb and ready to accept PROGRAM CARD")
					self.pcb.disp_job_details()				

				elif ifb.startswith('$DTA'):
					print("Getting Ready to accept DATA CARD")
					self.pcb.is_p = False
					self.pcb.is_d = True


				elif ifb.startswith('$END'):
					print("Loading current PCB in LOAD-QUEUE")
					self.pcb.disp_job_details()
					nw = PCB()
					nw = copy.copy(self.pcb)
					self.LQ.append(nw)
					self.pcb.__init__()

				else:
					if self.pcb.is_p:
						print("Adding PROGRAM to DRUM")
						drum_track = self.get_drum_track()
						self.D[drum_track] = ifb
						self.pcb.p_address[self.pcb.p_count] = drum_track
						self.pcb.p_count += 1
					elif self.pcb.is_d:
						print("Adding DATA to DRUM")
						drum_track = self.get_drum_track()
						self.D[drum_track] = ifb
						self.pcb.d_address[self.pcb.d_count] = drum_track
						self.pcb.d_count += 1

		#self.ebq.append(''.join([' ' for i in range(10)]))
		self.ebq.append(str((int(self.ebq[-1])+1)%10))
		self.IOI -= 4
		print("!-----------------------IR3()--------------------!")		

	def get_drum_track(self):
		for i in range(len(self.D)):
			if self.D[i][0] == '*':
				return i
		return -1

if __name__ == '__main__':
	op = open('op.txt','w')
	ph = phase3()
	#for line in ff:
	#	print (line)
	while ph.UT < 250 :
		if len(ph.ebq) !=0 and ph.CH1_flag == False:
			#print ('1')
			ph.start_CH1()
		if len(ph.ofbq) !=0 and ph.CH2_flag == False:
			#print ('2')
			ph.start_CH2()
		if len(ph.ifbq) !=0 and ph.CH3_flag == False:
			ph.case_task = 'IS'
			ph.start_CH3()
		
		if len(ph.LQ) != 0 and ph.CH3_flag == False:
			ph.case_task = 'LD'
			#print("#############################################")
			#ph.pcb_ld = copy.copy(ph.LQ[0])
			ph.start_CH3()

		ph.SIMULATION()
	
	op.close()

else:
	print('{} imported as module'.format(__name__))
