import random
import numpy as np
import matplotlib.pyplot as plt

consumerRatio = .1 
periods = 100
deter = .5
price = 1
people = 10000
consumerlist = []
Ratiolist = [consumerRatio]
changecounter = 0
changelist = []
finalutilityrange = []
freq = []
discreetlevel = 50
piraterange = []
nonpiraterange = []
price = 1

class Consumer(object):
	"""Initialize Consumers"""
	def __init__(self, fixed, social,pirate):
		self.social = social
		self.fixed = fixed
		self.pirate = pirate
	def __str__(self):
		return "<Social: %s. Fixed: %s. Piracy: %s.>" % (self.social,self.fixed,self.pirate)
	def decide(self,consumerRatio,deter):
		if self.pirate == False and self.social*consumerRatio + self.fixed > deter: 
			print("Has changed from non-buyer to Pirate. S={0}.F= {1}. P={2} " .format(self.social, self.fixed, self.pirate))
			global changecounter 
			changecounter += 1
			global directchange
			directchange += 1
			self.pirate = True
		elif self.pirate == True and self.social*consumerRatio + self.fixed < deter:
			print("Has changed from Pirate to non-buyer. S={0}.F= {1}. P={2} " .format(self.social, self.fixed, self.pirate))
			self.pirate = False
			global changecounter 
			changecounter += 1
			global directchange
			directchange -= 1
			self.pirate = False
		else:
			print("Has not changed. S={0}.F= {1}. P={2} " .format(self.social, self.fixed, self.pirate))
	def calculateutility(self,consumerRatio):
		util = self.social*consumerRatio + self.fixed
		return util

"""Sort and round array"""
def prepare(array):
	rounded = np.around(array,decimals=2)
	rounded.sort
	return rounded

"""Establish proportion of people who are consuming"""
def countpirates(list):
	truths = sum(1 for x in range(0,len(list)) if list[x].pirate == True)
	return truths

def show():
	print(finalutilityrange)
	print(Ratiolist)
	print(changelist)

"""Create an array of initialized consumers and add them to list"""
for x in range(0,people):
	fixed = random.uniform(0,1)
	social = random.uniform(0,1)
	if (social * consumerRatio + fixed) > deter:
		pirate = True
	else:
		pirate = False
	"Adds each consumer to the consumerlist"
	consumerlist.append(Consumer(fixed,social,pirate))

"""Calculates the ratio of pirates to consumers"""
consumerRatio = countpirates(consumerlist)/people

"""Go through the time periods updating the distribution"""
for i in range(0,periods):
	directchange = 0
	if i > 2 and changecounter == 0: 
		Ratiolist.pop()
		print('Breaking')
		break
	else: 
		changecounter = 0
		for x in range(0,len(consumerlist)):
			consumerlist[x].decide(consumerRatio,deter)
		print(changecounter)
		consumerRatio = countpirates(consumerlist)/people
		changelist.append(directchange)
		Ratiolist.append(consumerRatio)

"""Create array of Utility"""
for x in range(0,len(consumerlist)):
	utility = consumerlist[x].calculateutility(consumerRatio)
	finalutilityrange.append(utility)

"""Clean up utility array"""
finalutilityrange = prepare(finalutilityrange)
show()

idx = finalutilityrange < deter # Threshold to separate values

plt.hist([finalutilityrange[idx],finalutilityrange[~idx]],bins=100,normed=False,cumulative=False,color = ['b','r'])
plt.title("Histogram")
plt.xlabel("Utlity")
plt.ylabel("Probability")
plt.show()