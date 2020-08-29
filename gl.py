# Michael Chan 18562 
# Graficas por Computadora 
# gl

import struct
from obj import Obj 

def char(input):
	return struct.pack('=c', input.encode('ascii'))

def word(input):
	return struct.pack('=h', input)

def dword(input):
	return struct.pack('=l', input)

def glColor(r, g, b):
	return bytes([b, g, r])

BLACK = glColor(0, 0, 0)

class Render(object):
	def glInit(self, width, height):
		self.width = width
		self.height = height
		self.color = glColor(255, 255, 255)
		self.clearColor = glColor(0, 0, 0)
		self.glClear()

	def glColorPoint(self, r, g, b):
		self.color = glColor(round(r * 255), round(g * 255), round(b * 255))

	def glCreateWindow(self, width = 640, height = 480):
		self.width = width
		self.height = height

	def glClear(self):
		self.framebuffer = [
			[BLACK for i in range(self.width)]
			for j in range(self.height)
		]

	def glClearColor(self, r, g, b):
		self.clearColor = glColor(round(r * 255), round(g * 255), round(b * 255))
		self.framebuffer = [
            [clearColor for x in range(self.width)] for y in range(self.height)
        ]

	def pixel(self, x, y):
		self.framebuffer[y][x] = self.color

	def glFinish(self, filename):
		f = open(filename, 'bw')

		f.write(char('B'))
		f.write(char('M'))
		f.write(dword(54 + self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(54))

		f.write(dword(40))
		f.write(dword(self.width))
		f.write(dword(self.height))
		f.write(word(1))
		f.write(word(24))
		f.write(dword(0))
		f.write(dword(self.width * self.height * 3))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))
		f.write(dword(0))

		for x in range(self.height):
			for y in range(self.width):
				# print(x, y)
				f.write(self.framebuffer[x][y])

		f.close()

	def glLine(self, x1, y1, x2, y2):
		dy = abs(y2 - y1)
		dx = abs(x2 - x1)
		steep = dy > dx

		if steep:
		    x1, y1 = y1, x1
		    x2, y2 = y2, x2

		if x1 > x2:
		    x1, x2 = x2, x1
		    y1, y2 = y2, y1

		dy = abs(y2 - y1)
		dx = abs(x2 - x1)

		offset = 0
		threshold = dx

		y = y1
		for x in range(x1, x2 + 1):
		    if steep:
		        self.pixel(y, x)
		    else:
		        self.pixel(x, y)
		    
		    offset += dy * 2
		    if offset >= threshold:
		        y += 1 if y1 < y2 else -1
		        threshold += dx * 2

	def load(self, filename, translate, scale):
	    model = Obj(filename)
	    
	    for face in model.faces:
	      vcount = len(face)

	      for j in range(vcount):
	        f1 = face[j][0]
	        f2 = face[(j + 1) % vcount][0]

	        v1 = model.vertices[f1 - 1]
	        v2 = model.vertices[f2 - 1]
	        
	        x1 = round((v1[0] + translate[0]) * scale[0])
	        y1 = round((v1[1] + translate[1]) * scale[1])
	        x2 = round((v2[0] + translate[0]) * scale[0])
	        y2 = round((v2[1] + translate[1]) * scale[1])

	        self.glLine(x1, y1, x2, y2)