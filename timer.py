# -*- coding: iso-8859-1 -*-

import wx, time
from threading import Thread

# Ger namn och verision att använda så att man inte måste ersättta på flera ställen vid en änding
program = {"namn": "Timer","version": "1.0"}

class WorkerThread(Thread):
	"""Klass för att köra nedladdningarna i bakgrunden"""
	def __init__(self, parent):
		"""Init Worker Thread Class."""
		Thread.__init__(self)
		self.parent = parent

		#startar tråden
		self.start()
	

	def formatera_tid(self, tid_tagen):
		timmar = tid_tagen / 3600
		temp_kvar = tid_tagen % 3600
		minuter = temp_kvar / 60
		sekunder = temp_kvar % 60
		
		if timmar < 10:
			timmar = "0" + str(timmar)
		if minuter < 10:
			minuter = "0" + str(minuter)
		if sekunder < 10:
			sekunder = "0" + str(sekunder)
		
		return str(timmar) + ":" + str(minuter) + ":" + str(sekunder)


	def run(self):
		self.start_tid = int(time.time())
		self.sparade_sekunder = 0
		self.timer_running = True
		


		while True:
			if self.timer_running == True:
				tid_tagen = self.sparade_sekunder + int(time.time()) - self.start_tid
			elif self.timer_running == False:
				tid_tagen = self.sparade_sekunder
			

			self.parent.tid_kvar.SetLabel(self.formatera_tid(tid_tagen))

			time.sleep(1)
	
	def starta(self):
		self.timer_running = True
		self.start_tid = int(time.time())
	
	def pause(self):
		self.timer_running = False
		self.sparade_sekunder += int(time.time()) - self.worker.start_tid

class MyFrame(wx.Frame):
	def __init__(self, parent):
		wx.Frame.__init__(self, parent, -1, program["namn"], size=(150, 130), style=wx.CLOSE_BOX | wx.SYSTEM_MENU | wx.CAPTION | 0 | 0 | wx.MINIMIZE_BOX)
		self.panel = wx.Panel(self, -1)
		self.worker = None
		

		vbox = wx.BoxSizer(wx.VERTICAL)
		
		self.tid_kvar = wx.StaticText(self.panel, -1, '00:00:00')
		self.tid_kvar.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
		vbox.Add(self.tid_kvar, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.TOP | wx.BOTTOM, 3)
		
		self.knapp = wx.Button(self.panel, -1, 'Start', size=(120,50))
		self.knapp.SetFont(wx.Font(20, wx.SWISS, wx.NORMAL, wx.BOLD, False))
		vbox.Add(self.knapp, 0, wx.LEFT | wx.BOTTOM, 10)
		self.knapp.Bind(wx.EVT_BUTTON, self.starta_timern)
		
		self.panel.SetSizer(vbox)
		
	
		self.Bind(wx.EVT_CLOSE,  self.OnExit)


	def OnExit(self, event):
		self.Destroy()


	def pausa_timern(self, event):
		self.knapp.Bind(wx.EVT_BUTTON, self.starta_timern)
		self.knapp.SetLabel('Start')

		self.worker.pause()
	
	def starta_timern(self, event):
		# Förhindrar att flera trådar körs på samma gång
		if not self.worker:
				self.worker = WorkerThread(self)
		
		self.knapp.Bind(wx.EVT_BUTTON, self.pausa_timern)
		self.knapp.SetLabel('Pause')

		self.worker.starta()

		

#----------------------------------------------------
class MyApp(wx.App):
	def OnInit(self):
		frame = MyFrame(None)
		frame.Show(True)
		self.SetTopWindow(frame)
		return True

app = MyApp(0)
app.MainLoop()
