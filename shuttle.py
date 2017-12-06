import time
class Shuttle():
	def __init__(self, filename="shuttleSchedule.csv"):
		self.readFile(filename)
	def readFile(self, filename):
		fileHandle = open(filename, "r")
		lines = fileHandle.readlines()
		lines = [time.strptime(line.replace("\n",""),"%I:%M %p") for line in lines]
		fileHandle.close()
		self.lines = lines
	def getUpcoming(self):
		t = adjustedTime(time.localtime())
		output = []
		early = []
		for line in self.lines:
			if line > t:
				output.append(time.strftime("%I:%M %p", line))
			else:
				early.append(time.strftime("%I:%M %p", line))
		return output + early

def adjustedTime(t):
	return time.strptime(time.strftime("%I:%M %p",t), "%I:%M %p")

if __name__ == "__main__":
	s = Shuttle()
	print(s.getUpcoming())