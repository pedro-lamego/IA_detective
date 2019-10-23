
import math
import pickle
import time

  
class SearchProblem:

	def __init__(self, goal, model, auxheur = []):
		self.goal = goal
		self.model = model 
		self.auxheur = auxheur 
		#self.createNodes()
		pass

	def getCoords(self, index):
		return self.auxheur[index]

	def getAdjs(self, index):
		return self.model[index]

	def search(self, init, limitexp = 2000):
		g_cost = 0 

	def search(self, init, limitexp = 2000, limitdepth = 10, tickets = [math.inf,math.inf,math.inf]):
		return self.a_star(init, self.model, self.goal, tickets)
		return []

	def createAnswer(self, lst):
		path = []
		while lst[0].father:
			transports = []
			indexs = []
			joint = []
			for i in range(len(lst)):
				transports.append(lst[i].transport_index[0])
				indexs.append(lst[i].transport_index[1])
				print(lst[i].father)
				lst[i] = lst[i].father
			joint.append(transports)
			joint.append(indexs)
			path.append(joint)

		transports = []
		indexs = []
		joint = []
		for i in range(len(lst)):
			indexs.append(lst[i].transport_index[1])
		joint.append(transports)
		joint.append(indexs)
		path.append(joint)

		return path
	
	def createNodes(self):
		node_list = []
		for i in range(0, 114):
			node_list.append(Node(i, None, 0, 0))
		
		return node_list
	
	#auxiliary functions
	def start_node_answer(self, list):
		return [[], [list[0].index]]

	def a_star(self, init, model, goal, tickets):
		
		openset = []
		currents = []
		for i in range(len(init)):
			currents.append(Node([[], init[i]], None, tickets))
		
		for i in range(len(init)):
			listCurrent = []
			listCurrent.append(currents[i])
			openset.append(listCurrent)
		

		while openset:
			for j in range(len(currents)):
				min = 1000
				for node in openset[j]:  #just a node
					value_f = node.g + self.heuristic(goal[j], node)
					"""if(node.transport_index[1] == currents[j].transport_index[1] and min == value_f):
						print(node.transport_index[1])
						print(currents[j].transport_index[1])
						min = value_f
						currents[j] = node
					else:"""
					if(min > value_f):
						min = value_f
						currents[j] = node
						#print("My index is " + str(node.transport_index[1]) + ". My transport is " + str(node.transport_index[0]) + " and my father is " + str(node.father) + "")
			
			#check if all in goal
			flag_all_in_goal = 1
			for i in range(len(currents)):
				if currents[i].transport_index[1] != goal[i]:
					flag_all_in_goal = 0
					break
			
			#create final answer
			if(flag_all_in_goal):
				print(currents)
				path = self.createAnswer(currents)
				print(path)
				return path[::-1]
		
			#remove from the openset list
			print(openset)
			for i in range(len(currents)):
				for node in openset[i]:
					if(node == currents[i]):
						openset[i].remove(node)
	
			
			for i in range(len(currents)):
				for node in self.neighbors(currents[i].transport_index[1]):
					node = Node(node, currents[i], currents[i].tickets)
					node.reduceTickets(node.transport_index[0])
					if(node.tickets[node.transport_index[0]] < 0):
						continue
					flag = 0

					for j in range(len(openset)):
						for node_open_set in openset[j]:
							if(node_open_set.transport_index[1] == node.transport_index[1]):
								flag = 1
								break	
					
					if flag:
						new_g = currents[i].g + 1
						if node.g > new_g:
							node.g = new_g
							node.father = currents[i]
					else:
						node.g = currents[i].g + 1
						node.h = self.heuristic(goal[i], node)
						node.father = currents[i]
						openset[i].append(node)

	def heuristic(self, goal, node):

		h2 = self.calculateH2(node.transport_index[0])
		h3 = self.calculateH3(goal, node.transport_index[1])

		return h2 + h3

	def calculateH2(self, node):
		if(node == 0): 
			return 3
		elif(node == 1):
			return 2
		else:
			return 1
	
	def calculateH3(self, goal, node):
		x1 = self.auxheur[node - 1][0]
		x2 = self.auxheur[goal - 1][0]
		y1 = self.auxheur[node - 1][1]
		y2 = self.auxheur[goal - 1][1]
		return math.sqrt((x2 - x1)**2 + (y2-y1)**2) / 120
	
	def neighbors(self, index):
		return self.model[index] 

class Node:
	def __init__(self, transport_index, father, tickets):
		self.transport_index = transport_index
		self.father = father
		self.tickets = tickets.copy()
		
		self.g = 0
		self.h = 0
		self.f = 0

	def __repr__(self):
		return str(self.transport_index[1])

	def getFather(self):
		return self.father

	def getIndex(self):
		return self.index
		
	def getG(self):
		return self.g
		
	def getH(self):
		return self.h 
	
	def getF(self):
		return self.f
	
	def reduceTickets(self, transport):
		self.tickets[transport] -= 1
