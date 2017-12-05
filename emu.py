path = 'Donkey Kong (Japan).nes'
class NES:
	def __init__(self, path):
		self.file = open(path, 'rb').read()
		self.header = self.file[:16]
		pointer = 16

		#Check for valid file
		try:
			assert self.header[:4] == b'NES\x1a'
		except:
			print('Incorrect File Header.')
			quit()

		# ROM and RAM Sizes	
		prgRomSize = self.header[4]*16384
		chrRomSize = self.header[5]*8192
		self.prgRamSize = self.header[8]*8192
		if self.prgRamSize == 0:
			self.prgRamSize = 8192

		#Flags 6-9
		flags6 = self.header[6]
		flags7 = self.header[7]
		flags9 = self.header[9]
		self.mirroring = 'h'
		if flags6 % 2 == 1:
			self.mirroring = 'v'
		self.batteryRam = (flags6 >> 1) % 2
		self.isTrainer = (flags6 >> 2) % 2
		self.ignoreMirror = (flags6 >> 3) % 2
		self.tv = 'NTSC'
		if flags9 % 2 == 1:
			self.tv = 'PAL'

		#Mapper No.
		m1 = (flags6 >> 4)
		m2 = (flags7 >> 4)
		self.mapper = m2 << 4 + m1
		
		#Check for Trainer
		if self.isTrainer:
			self.Trainer = self.file[pointer:pointer+512]
			pointer += 512

		#Initialize CPU Memory
		self.RAM = [0]*0x10000

		#Load ROMs into memory
		self.prgROM = self.file[pointer:pointer+prgRomSize]
		pointer += prgRomSize
		self.chrROM = self.file[pointer:pointer+chrRomSize]
		pointer += chrRomSize

		self.RAM[0x8000:] = self.prgROM * (0x8000//prgRomSize)
		self.memPointer = 0

	def run(self):
		reset_vector = (self.RAM[0xfffc] << 8) + self.RAM[0xfffd]
		self.memPointer = reset_vector
		print(self.RAM[self.memPointer])
		

n = NES(path)
n.run()