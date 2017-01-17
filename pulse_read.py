import numpy as np
import h5py
from scipy import signal
import struct;
import sys, os
import glob
import scipy.optimize as opt
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib as mpl
from shutil import copyfile
mpl.rc('figure', facecolor = 'w')


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#read in noise data
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
class Res():

	def __init__(self):
		self.flux = []

	def readFile(self, filename):
		self.filename = filename
		datafile = open(filename)
		data = []
		for line in datafile:
			data.append(line)
		datafile.close()

		#the first 35 lines are file headers, after that are pulse data
		y = []
		for i in range(35, len(data)):
			y.append(float(data[i].split()[1]))
		y = np.array(y)
		self.flux = y/2./np.pi #convert phase to flux


		#the pusles are saved in 500-point sections
		#read them into an array
		l = 501
		N = len(self.flux)/l
		self.pulseNum = N
		print 'pulse number:', N
		self.pulseArray = np.empty((N, l-1))
		for i in range(N):
			onePulse = self.flux[i*l : (i+1)*l-1]
			self.pulseArray[i] = onePulse

	def MatchedFilter(self):
		self.pulseArray = self.pulseArray[: , 230:450] #cut out the pulse section for correlation, not necessary
		self.peak = np.empty(self.pulseNum) #initialize a blank array to save correlation results

		#correlation method is used for this matched filter
		#the Ka and Kb pulses are using two separate templates, each template is from a pulse data (yes I'm not using an average template here). 
		#pulse#0 is a Ka pulse, and pulse#19 is a Kb phase. They are used as templates
		for i in range(self.pulseNum):
			if abs(self.pulseArray[i]).max()<0.9:
				temp = self.pulseArray[0]/np.sqrt(np.sum(self.pulseArray[0]**2))
				self.peak[i] = np.correlate(self.pulseArray[i], temp, 'full').max()
	
			else:			
				temp = self.pulseArray[19]/np.sqrt(np.sum(self.pulseArray[19]**2))
				self.peak[i] = np.correlate(self.pulseArray[i], temp, 'full').max()



	def plotHist(self):
		self.low = 4.5 #histogram bin boundary
		self.high = 5.
		self.binNum = 50
		self.hist, bin_edges = np.histogram(self.peak, bins=self.binNum, range=(self.low, self.high))
		self.bin = bin_edges[1:]

		#plt.plot(self.bin, self.hist, linestyle='', marker='.', color=color)#, label=Resname+', '+str(self.pulseNum)+' pulses')
		color = 'r'
		plt.hist(self.peak, bins=self.binNum, range=(self.low, self.high), edgecolor=color, facecolor = color, alpha = .5, label=str(self.pulseNum)+' pulses')
		plt.xlim(self.bin[0], self.bin[-1])
		plt.xlabel('pulse correlation', size = 15)
		#plt.xlabel(r'pulse peak height [$\Phi_0$]', size = 15)
		plt.ylabel('Num of Pulse', size = 15)
		#plt.suptitle('300 bins')
		plt.legend(loc='upper right')

	def plotPulse(self):
		for i in range(self.pulseNum-1):
			plt.plot(self.pulseArray[i], linestyle='-', marker='.', alpha=0.3)#, color=color)
		plt.plot(self.pulseArray[-1], label=str(self.pulseNum)+' pulses')

		plt.legend(loc='lower right')
		plt.ylabel(r'$\Phi_0$', size = 15)



filename = 'Res-8_Att1_10_Att2_40_0.075K_Circle.PulseMux'
print filename
Res24 = Res()
Res24.readFile(filename)
#Res24.plotPulse()
Res24.MatchedFilter()
Res24.plotHist()


plt.show()
