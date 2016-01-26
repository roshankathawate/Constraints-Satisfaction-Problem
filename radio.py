# Assignment 4 - Constraints satisfaction Problem
# B551 Fall 2015
# NAME:-	ROSHAN KATHAWATE
# USER ID:- rkathawa
# Problem formulation : Divided problem in three different parts, first part is to read all 
# states from a given file and maintaining a list of their neighbors, their domain and given constraints.
# Second part is to create a graph on the go. To creat a graph i am using most constraining variable from a given states
# and then for next node I apply same MCV logic and creates graph out of this.
# Third and most interesting part is to forward check constraints, this is done by checkCSP function.
# This function takes a state and its assigned value and removes that value from all its neibhouring states.
# While doing so if it find that any neighbouring state is going out of domain then it returns.
# If assigned domain value is failed then I go for other values and do forward checking again.
# Another important part of the solution formulation is to maintaing and doing backtracking.
# Backtracking happens when any particular variable goes out of domain values. In such a case I go back to that node
# and reassign new domain. Also, when backtradcking happens we need to remove those nodes from visited list and also we have 
# reassign all removed values from the domain.
# values to it and does forward checking with all its neighbours.
#Observation: +---------------------------------------------+
#			  | constraints         |     # of backtracks   |	
#			  +---------------------------------------------+
#			  | adjacent-states     |       0               |
#             +---------------------------------------------+
#             | legacy-constraints-1| 0,some time got 3     |   
#             +---------------------------------------------+
#			  | legacy-constraints-3|       0               |	
#			  +---------------------------------------------+
# Problems faced: Implementing backtracking and validating out put.
# Assumptions: There will be no neighbors for two states.also, in backtracking I expand the domain of a parent to include 
# the complement of the assigned value and take help of the implemented algorithm to recursively rectify the impact on the neighboring states.
# While less efficient compared to altering the parents domain to the next valid value, this approach is working for the given constraint files. 
# Also, if we implement arc consistancy number of backtracks will reducce further.
import sys
import 	operator

# Read constraints from a given file and adjacent-states
def processCSP():
	f1 = open('legacy-constraints-3','r')
	for line1 in f1:
		st = line1.split()
		Domain[st[0]]=[st[1]]
		constraints.append(st[0])

	f1.close()

	f = open('adjacent-states','r')
	visited =[]
	noOfNeighbors = {}
	variables = []
	for line in f:
		states = line.split()
		listOfneighbors = []
		#node = Node(states[0])
		for i in range(1,len(states)):
			#node.neighbors.append(states[i])
			listOfneighbors.append(states[i])	 
		unassignedVariables[states[0]] = listOfneighbors
		noOfNeighbors[states[0]] = len(listOfneighbors)
		variables.append(states[0])
		
		if states[0] not in Domain:
			Domain[states[0]] = ['A','B','C','D']
			# print states[0],"=>",Domain[states[0]]
	f.close()
	
	count = 1
	# print "variables:",variables
	#As two states has no neighbours loop over 48 times
	while(count <49):
		mcv = getMCV(variables,noOfNeighbors,visited)
		# print "Next node:",mcv
		if unassignedVariables[mcv] != []:
			variables = unassignedVariables[mcv]
			# print "Next List:",variables
		if mcv not in visited:
			visited.append(mcv)
			count = count +1
	# for i in visited:
	#  	print i,"=>",
	

	count = 1
	d = ['A','B','C','D']
	x = 0
	assigned.append(visited[0])
	Domain[visited[0]] = d
	while(count < 49):
		result = checkCSP(visited[count -1],d[x],assigned)
		if result == False:
			# print "Failed",Domain[visited[count -1]]
			x = (x+1)%len(Domain[visited[count -1]])
			if len(Domain[visited[count -1]])==1:
				global backtrack
				backtrack = backtrack + 1
				s = set(['A','B','C','D']).difference(set(Domain[visited[count -1]]))
				Domain[visited[count -1]]= list(s)
				x = 0
				d = Domain[visited[count -1]]
		else:
			Domain[visited[count -1]]=[d[x]]
			count = count + 1
			if count < 49	:
				# print "Dommmmmain:->",visited[count -1],"=>",Domain[visited[count -1]]
				d = Domain[visited[count -1]]
				x = 0
	printOutPut()
	# for i in Domain:
	#  	print i,"===>",Domain[i]
	# print "TOtal backtrack is:",backtrack

#get city which has most number of neighbors or has only one domain value
def getMCV(variables,noOfNeighbors,visited):
	listneighbors = {}
	if variables != []:
		for i in variables:
			if i not in visited:
				if i in constraints:
					return i
				else:
					#print i,"===>",noOfNeighbors[i]
					listneighbors[i]= noOfNeighbors[i]
	if not listneighbors :
		for i in visited:
			s = set(unassignedVariables[i]).difference(set(visited))
			if s:
				# print "Parent :",i,"child:",s
				return i
	else:
		l = max(listneighbors.iteritems(),key=operator.itemgetter(1))[0]
		return l
	
#Do forward checking 	
def checkCSP(node,domainValue,assigned):
	result = True
	for i in unassignedVariables[node]:
		if domainValue in Domain[i]:
			Domain[i].remove(domainValue)
		# print "Domain of ",i,"=>",Domain[i]
		if(Domain[i] != []):
			result = True
			assigned.append(i)
		else:
			result = False
			# print "Allocating again"
			for i in unassignedVariables[node]:
				if domainValue not in Domain[i]:
					Domain[i].append(domainValue)
				assigned.remove(i)
				# print "New Doamin:",i,"=>",Domain[i]
			break
	return result

def printOutPut():
	global backtrack
	f = open('adjacent-states','r')
	f1 = open('results.txt','w')
	for line in f:
		states = line.split()
		f1.write(states[0]+" "+Domain[states[0]][0]+"\n")
			# print Domain[states[i]][0],
		# print
	f.close()
	f1.close()
	print "Number of backtracks: ",backtrack
unassignedVariables = {}
Domain = {}	
assigned = []
constraints = []
backtrack = 0
processCSP()
