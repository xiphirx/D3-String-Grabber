import struct
from collections import namedtuple

class stlFile:
	sizeDesc = 0x50
	sizeHeader = 0x38
	sizeMPQHeader = 0x10
	sizeRecord = 0x10
	def init(self, filePath):
		try:
			self.fileHandle = open(filePath, 'rb')
		except IOError:
			print 'stlFile: That .stl file does not exist or is read protected'
		else:
			if not self.readHeader():
				print 'Error: this is not a correct STL file!'
			else:
				self.readStrings()
				
	def readHeader(self):
		stlHeader = namedtuple('stlHeader', 'magic unk1 free1 unk2 free2 free3 free4 unk3 dataStart free5')
		self.header = stlHeader(*struct.unpack('@IILIILLIIL', self.fileHandle.read(self.sizeHeader)))
		if (not self.header.magic == 0xDEADBEEF):
			return False
		return True
	
	def readStrings(self):
		stlRecord = namedtuple('stlRecord', 'type free1 start length')
		stlDesc = namedtuple('stlDesc', 'name value add1 add2 end')
		numOfRecords = (self.header.dataStart - self.sizeHeader) / self.sizeDesc
		self.desc = []
		self.stringList = []
		for i in range(numOfRecords):
			desc = []
			string = []
			for j in range(5):
				self.fileHandle.seek(i * self.sizeDesc + self.sizeHeader + j * self.sizeRecord)	
				record = stlRecord(*struct.unpack('@IIII', self.fileHandle.read(self.sizeRecord)))
				self.fileHandle.seek(record.start + self.sizeMPQHeader)
				string.append(self.fileHandle.read(record.length))
				desc.append(record)
			sDesc = stlDesc(desc[0], desc[1], desc[2], desc[3], desc[4])
			self.desc.append(sDesc)
			self.stringList.append(string)
