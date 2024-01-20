import random
from unittest import result
import matplotlib
import numpy as np
import math
import sys
import matplotlib.pyplot as plt


ALPHA = 0.03
GAMMA = 1
LAMBDA = 0.9
F_BASE = 4 


class EnvironmentMC:
	
	def __init__(self, maxEps=500, stateDim=2, numActions=3):
		self.maxEps = maxEps
		self.stateDim = stateDim
		self.numActions = numActions

		self.TS = 20000
		self.minX = -1.2
		self.maxX = 0.5
		self.minXDot = -0.07
		self.maxXDot = 0.07
		self.state = np.zeros(stateDim)
		self.newEpisode()
	
	def bound(self, x, minV, maxV):
		return min(maxV, max(x, minV))

	def normalize(self, x, minV, maxV):
		return (x - minV)/(maxV - minV)

	# require : returns the current state
	def getState(self):
		ret = np.zeros(self.stateDim)
		ret[0] = self.normalize(self.state[0], self.minX, self.maxX)
		ret[1] = self.normalize(self.state[1], self.minXDot, self.maxXDot)
		return ret

	
	def transition(self, action):
		self.count += 1
		val = action - 1
		self.state[1] = self.bound(self.state[1] + 0.05 * val - 0.005 * np.cos(3 * self.state[0]), self.minXDot,self.maxXDot)
		self.state[0] += self.state[1]
		if (self.state[0] < self.minX):
			self.state[0] = self.minX
			self.state[1] = 0
		if (self.state[0] > self.maxX):
			self.state[0] = self.maxX
		return -1

	
	
	def isTS(self):
		if self.count >= self.TS or self.state[0] >= self.maxX:
			return True
		return False

	
	
	def newEpisode(self):
		self.state[0] = -0.5
		self.state[1] = 0
		self.count = 0
		return





class TD:
	def __init__(self, stateDim=2, numActions=3):
		self.basis = F_BASE**stateDim
		self.numActions = numActions
		self.A = np.zeros((self.basis, self.basis))
		self.B = np.zeros(self.basis)
		self.E = np.zeros(self.basis)
		

		self.FMat = np.zeros((self.basis, stateDim))
		self.FRow = np.zeros(stateDim)
		for x in range(self.basis):
			self.FMat[x] = self.FRow
			self.getNextFRow(stateDim)

	def getNextFRow(self, stateDim):
		for i in range(stateDim):
			self.FRow[i] += 1
			if (self.FRow[i] <= F_BASE - 1):
				break
			self.FRow[i] = 0
		return

	
	def getFVec(self, state):
		return np.cos(np.dot(self.FMat, state) * math.pi)

	
	def getAction(self, state):
		return random.randint(0, self.numActions - 1)

	
	def update(self, curState, curAction, reward, nextState=None, nextAction=None):
		curFVec = self.getFVec(curState)
		self.E = GAMMA * LAMBDA * self.E + curFVec
		if nextAction is not None:
			nextFVec = self.getFVec(nextState)
			self.A += np.outer(self.E, (curFVec - GAMMA * nextFVec))
		else:
			self.A += np.outer(self.E, curFVec)
		self.B += self.E * reward
		return

	
	def newEpisode(self, curState):
		self.E = np.zeros(self.basis)
		self.E = self.getFVec(curState)
		return

	
	def getBeta(self):
		return np.dot(np.linalg.pinv(self.A), self.B)

def check():
	if not isinstance(F_BASE, int) or F_BASE < 1:
		sys.exit("F_BASE must be int > 0")
	if LAMBDA < 0 or LAMBDA > 1:
		sys.exit("invalid value of lambda")
	if GAMMA < 0 or GAMMA > 1:
		sys.exit("invalid value of lambda")

def runEnv(envName):
	env = None
	if envName is "mountainCar":
		env = EnvironmentMC()
	else:
		print("Select proper environment")
		return
	td = TD(env.stateDim, env.numActions)
	result = np.zeros(env.maxEps)
	for ep in range(env.maxEps):
		env.newEpisode()
		result[ep] = 0
		curGamma = 1
		curState = env.getState()
		curAction = td.getAction(curState)
		td.newEpisode(curState)
		while True:
			reward = env.transition(curAction)
			result[ep] += (curGamma * reward)
			curGamma *= GAMMA
			if env.isTS():
				td.update(curState, curAction, reward)
				break
			newState = env.getState()
			newAction = td.getAction(newState)
			td.update(curState, curAction, reward, newState, newAction)
			curAction = newAction
			curState = newState
	
	print(result)
	print('\n\n\n')
	print(td.getBeta())
	return
	

if __name__ == '__main__':
	check()
	runEnv("mountainCar")

