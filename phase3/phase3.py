from phase2.phase2 import phase2

class phase3(phase2):

if __name__ == '__main__':
	fp = open('inp.txt','r')
	ff = iter(fp.read().split('\n'))
	fp.close()
	op = open('op.txt','w')
	ph = phase3()
	ph.LOAD()
	op.close()
else:
	print('{} imported as module'.format(__name__))
