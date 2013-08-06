#!/usr/bin/python
# -*- coding: utf-8 -*-

import cherrypy
import serial
import io
import threading
import simplejson as json
import os

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
	def api(self):
		cherrypy.response.headers['Content-Type']= 'application/json'	
		return json.dumps({"temperature": temperature})

_thread = threading.Thread(target=arduinoReceive)
_thread.setDaemon(True)
_thread.start()

current_dir = os.path.dirname(os.path.abspath(__file__)) 

conf = {'global': {'server.socket_host': '0.0.0.0',
				'server.socket_port': 8080,
				'tools.encode.on': True,
				'tools.encode.encoding': "utf-8" },
		'/index': {	'tools.staticfile.on': True,
					'tools.staticfile.filename': os.path.join(current_dir, 'index.html')},
		'/static': {'tools.staticdir.on': True,
					'tools.staticdir.dir': os.path.join(current_dir, 'static'),
					'tools.staticdir.content_types': {'js': 'text/javascript',
														'css': 'text/css'}}}

#cherrypy.server.socket_host = "0.0.0.0";
cherrypy.quickstart(SlushServer(), config = conf )
