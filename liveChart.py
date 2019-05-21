import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import time
import matplotlib

#matplotlib.use('GTKAgg',warn=False, force=True)

class live_plot ():
	flag_need_close = False

	def __init__(self):
		self.plots = []
		self.cases = [1, 2, 3, 4, 5, 6, 7, 8]
		self.y = []
		for i in range(8):
			self.y.append([])
		self.figsize = (10, 8)
		self.cols = 2
		self.rows = 4
		self.fig1, self.axs = plt.subplots(self.rows, self.cols, figsize=self.figsize, constrained_layout=True)
		self.axs = self.axs.flat
		self.lines = []

	def close (self):
		self.flag_need_close = True

	def add_data(self, emg):
		for ind, val in enumerate(emg):
			self.y[ind].append(val)

	def handle_close(self, evt):
		print("JUST CLOSE")
		self.flag_need_close = True

	def show_plots(self):
		self.flag_need_close = False
		self.fig1.canvas.draw()
		plt.show(block=False)
		for ax, case in zip(self.axs, self.cases):
			ax.set_title('%s' % str(case))
			line, = ax.plot(range(len(self.y[case - 1])), self.y[case - 1], markevery=case)
			self.lines.append(line)
			ax.set_ylim([0, 1500])
		self.fig1.canvas.mpl_connect('close_event', self.handle_close)
		plt.pause(1)


	def update_plots(self):
		while not self.flag_need_close:
			try:
				for ind, line in enumerate(self.lines):
					if len(self.y[ind]) > 2000:
						self.y[ind] = self.y[ind][-2000:] 
					line.set_ydata(self.y[ind])
					line.set_xdata(range(len(self.y[ind])))
					self.axs[ind].relim()
					self.axs[ind].autoscale_view(True,True,False)
				self.fig1.canvas.draw()
				plt.pause(1)
			except:
				pass
		
			
