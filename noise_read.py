import numpy as np
import h5py
from scipy import signal
import struct;
import sys, os
import glob
import scipy.optimize as opt
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy.signal import welch
mpl.rc('figure', facecolor = 'w')


class Res():
	def __init__(self):
		self.time = []
		self.flux = []

	def readFile(self, filename):
		datafile = open(filename)
		for data in datafile:
			self.time.append(float(data.split()[0]))
			self.flux.append(float(data.split()[1]))
		self.time = np.array(self.time)
		self.flux = np.array(self.flux)


	def calPSD(self):
		#the flux ramp rate is 50 kHz
		fs = 50e3
		nperseg = 25000 #length of window
		window = 'hanning'
		self.ff_ns, self.flux_psd = signal.welch(self.flux, fs = fs, window = window, nperseg = nperseg, noverlap=0, return_onesided=True)

		
	def plotPSD(self):
		phaseAxis.plot(self.time, self.flux*1e3, alpha=.5)
		phaseAxis.set_xlabel('Time [s]')
		phaseAxis.set_ylabel('m$\Phi_0$')

		psdAxis.loglog(self.ff_ns, np.sqrt(self.flux_psd)*1e6, alpha=.5)
		psdAxis.set_xlabel('Freq [Hz]')
		psdAxis.set_ylabel(r'Flux Noise [$\mu \Phi_0/\sqrt{Hz}$]')

		#psdAxis.set_ylim(1e0, 1e2)
		#psdAxis.set_xlim(1e0, 3e4)



fig = plt.figure()
phaseAxis = fig.add_subplot(211)
psdAxis = fig.add_subplot(212)

filename = 'Res-8.noiseflux'
fluxFile = Res()
fluxFile.readFile(filename)
fluxFile.calPSD()
fluxFile.plotPSD()

plt.show()

