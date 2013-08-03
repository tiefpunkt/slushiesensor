#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
import serial
import io
import threading
import simplejson as json

temperature = [ 0,0,0 ]

def arduinoReceive():
	global temperature
	serialIn = serial.Serial('/dev/ttyACM0', 9600, bytesize=8, parity='N', stopbits=1, timeout=0)
	sio = io.TextIOWrapper(io.BufferedRWPair(serialIn, serialIn))
	while True:
		line = sio.readline()
		if ";" in line:
			temperature_temp = line.rstrip().split(";")
			try:
				temperature = map(float, temperature_temp)
			except ValueError:
				pass

class SlushServer(object):
	
	@cherrypy.expose
	def index(self):
		return '''
<html>
<head>
<title>RaumZeitLabor Slush Machine</title>
</head>
<body>
<h1>RaumZeitLabor Slush Machine</h1>
Come grab some slush at the ICMP village!
<h2>Temperatures</h2>
<ul>
<li>Chamber 1: ''' + str(temperature[0]) + '''°C</li>
<li>Chamber 2: ''' + str(temperature[1]) + '''°C</li>
<li>Chamber 3: ''' + str(temperature[2]) + '''°C</li>
</ul>
</body>
</html
'''
	
	@cherrypy.expose
	def api(self):
		return json.dumps({"temperature": temperature})

_thread = threading.Thread(target=arduinoReceive)
_thread.setDaemon(True)
_thread.start()

cherrypy.server.socket_host = "0.0.0.0";
cherrypy.quickstart(SlushServer())
