#!/usr/bin/python

import cups
from os import listdir, remove
import  os.path
import urllib2
import sys
import time
from datetime import datetime
from evdev import InputDevice
from select import select
import ConfigParser
try:
	import piglow
except:
	pass

class PassPrinter:
	conn = None
	printer = None
	tmpLocation = "./"
	keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX"
	rfidDevice = None
	rfidPath = '/dev/input/event0'
	URL = ""
	configFileLocation = '/etc/parkomatic/parkomatic.conf'
	config = None
	piGlowEnable = False

	def __init__(self):
		self.configFileLocation = os.getenv('CONFFILE', self.configFileLocation)
		self.config = ConfigParser.ConfigParser()
		#Try to load config file
		
		if self.configFileLocation not in self.config.read(self.configFileLocation):
			self.configFileLocation = None
			
		#Try to set rfid input path from config file.
		try:
			self.rfidPath = self.config.get('Parkomatic', 'rfid_input_path')
		except: 
			pass
		
		#Try to set destination URL from config file.
		try:
			self.URL = self.config.get('Parkomatic', 'url')
		except:
			pass
		
		#Try to set tmp path from config file.
		try:
			self.tmpLocation = self.config.get('Parkomatic', 'tmp_path')
		except:
			pass
		
		try:
			piglow_val = self.config.get('Parkomatic', 'piglow')
			if piglow_val == "enable":
				self.piGlowEnable = True
		except:
			 pass
		
		#Try to create the tmp location if it doesn't exist
		if not os.path.exists(self.tmpLocation):
			os.makedirs(self.tmpLocation)
		
		#Make a connection to the CUPS server
		try:
			self.conn = cups.Connection()
		except:
			print "ERROR: CUPs not available"
			#Sleep for 5 seconds as repeatedly attemping to connect to CUPs seems to make it hard for cups to start initially.
			time.sleep(5)
			sys.exit(1)
			
		printers = self.conn.getPrinters()
		if len(printers) == 0:
			print "ERROR: No printers available"
			time.sleep(5)
			sys.exit(1)
		#Get the first printer in the list
		self.printer = printers.keys()[0]
		
		#Create the RFID input device
		self.rfidDevice = InputDevice(self.rfidPath)
		print "STARTED: Waiting for input."
		if self.piGlowEnable:
			piglow.auto_update = True;
			piglow.all(0)
			piglow.red(255)
			time.sleep(0.1)
			piglow.red(0)
			piglow.green(255)
			time.sleep(0.1)
			piglow.green(0)
			piglow.yellow(255)
			time.sleep(0.1)
			piglow.white(255)
			piglow.yellow(0)
			time.sleep(0.1)
			piglow.white(0)
			

	def getImage(self, keyNum):
		filename = self.tmpLocation + str(keyNum) + ".png"
		if self.piGlowEnable:
			piglow.all(0)
			piglow.yellow(255)
		if (os.path.isfile(filename)):
			if (datetime.fromtimestamp(os.path.getctime(filename)).date() < datetime.today().date()):
				print "DELETE: "+str(keyNum)+", [File older than today]"
				os.remove(filename)
			else:
				print "CACHED: "+str(keyNum)+" [Returning cached file]"
				return filename
			
		if not self.URL:
			print 'ERROR: Unable to locate file, and URL fetching not configured'
			return False	
		
		if (self.URL and "<CARDNUM>" not in self.URL):
			print 'ERROR: <CARDNUM> placeholder not found in URL config'
			return False
		
		try:
			print "GET: "+str(keyNum)+" [Downloading new file]"
			url = self.URL.replace('<CARDNUM>', str(keyNum))
			uh = urllib2.urlopen(url)
		except:
			print "NOTFOUND: "+str(keyNum)+" [Server responded non-200]"
			return False
		CHUNK = 16 * 1024
		with open(filename, 'wb') as f:
			while True:
				chunk = uh.read(CHUNK)
				if not chunk: break
				f.write(chunk) 
			f.close()
		print "WROTE: "+filename
		return filename
	def printFile(self, filename):
		if self.piGlowEnable:
			piglow.all(0)
		if filename is not False:
			if self.piGlowEnable:
				piglow.green(255)
			print "PRINT: "+ str(filename) + " [Sent to printer]"
			self.conn.printFile(self.printer, filename, "Test", {"CutMedia": "2"})
		else:
			if self.piGlowEnable:
				piglow.red(255);
		if self.piGlowEnable:
			time.sleep(2)
			piglow.all(0)
			piglow.show()

	def mainLoop(self):
		lastKey = 0
		currentKey = ""

		while True:
			r,w,x = select([self.rfidDevice], [], [])
			for event in self.rfidDevice.read():
			        if event.type==1 and event.value==1:
					if (lastKey + 5) < time.time():
						currentKey = ""
					if self.keys[event.code] == "X":
						print "READ: " + str(int(currentKey))
						self.printFile(self.getImage(int(currentKey)))
						currentKey = ""
					elif self.keys[event.code] in "0123456789":
						currentKey = currentKey + self.keys[event.code]
					lastKey = time.time()


pp = PassPrinter()
pp.mainLoop()

