
import math


class Systems(object):
	def __init__(self, *args):
		"""takes in equations and converted them into matrices
		assumes all equations entered are simplified"""
		keys = []
		for v in args:
			print("Terms ARE:", v.getTerms(), "-"*100)
			for term in v.getTerms():
				print("Term in getTerms", term)
				print("@"*100)
				print("TERM IN EQ:", term)
				if term.getLitCoef() not in keys:
					print("term not in keys", term)
					print(keys, "before")
					keys.append(term.getLitCoef())
					print(keys, "after")
		matrix = []
		i = 0
		for eq in args:
			matrix.append([])
			matrix_form = eq.getVarsMatrix()
			print("Matrix FORM", eq.getVarsMatrix())
			for var in keys:
				try:
					print(matrix, matrix[i])
					matrix[i].append(matrix_form[var])
				except KeyError:
					matrix[i].append(0)
			matrix[i].append(matrix_form[""])
			i += 1
		print("number of equations", len(matrix), "number of vars", len(matrix[0])-1)
		print(keys)
		self.matrix = matrix
		self.keys = keys
	
	# getters
	
	def getMatrix(self):
		return self.matrix
	
	def getKeys(self):
		return self.keys
	
	def getRow(self, rnum):
		m = self.getMatrix()
		return m[rnum]
	
	def getVarVals(self, coln):
		col = [i[coln] for i in self.getMatrix()]
		return col
	
	def getEq(self, num):
		"""num is a number between 0 and len(self.matrix)-1"""
		m = self.matrix
		try:
			return m[num]
		except KeyError:
			raise ValueError("num is greater than the equations in the matrix. len(matrix): " + str(len(m)))

	# setters
	
	def setMatrix(self, m):
		self.matrix = m
	
	def setEq(self, num, eq):
		"""num is a number between 0 and len(self.matrix)-1
		eq is an equation"""
		m = self.matrix
		try:
			m[num] = eq
		except KeyError:
			raise ValueError("num is greater than the equations in the matrix. len(matrix): " + str(len(m)))
		self.setMatrix(m)
		
	# row operations
	
	def multRow(self, rnum, n):
		m = self.getMatrix()
		m[rnum] = [n*i for i in m[rnum]]
		self.setMatrix(m)
	
	def getMulted(self, rnum, n):
		m = self.getMatrix()
		multed = [n*i for i in m[rnum]]
		return multed
	
	def addRows(self, rnum1=None, rnum2=None, row1=None, row2=None):
		assert (rnum1 is not None or row1 is not None) and (row2 is not None and rnum2 is not None), "either rows or row indexes must be given"		
		m = self.getMatrix()
		if rnum1 is not None:
			row1 = self.getRow(rnum1)
		if rnum2 is not None:
			row2 = self.getRow(rnum2)
		outrow = []
		for i in range(len(row1)):
			outrow[i] = row1[i] + row2[i]
		return outrow
	
	def addToRow(self, rnum1=None, rnum2=None, row1=None, row2=None):
		"""add row2 to row1 and return nothing"""
		assert rnum1 is not None and (rnum2 is not None or row2 is not None), "index must be provided"		
		m = self.getMatrix()
		row1 = m[rnum1]
		if rnum2 is not None:
			row2 = m[rnum2]
		for i in range(len(row1)):
			row1[i] += row2[i]
		m[rnum1] = row1
		self.setMatrix(m)
	
	def subRow(self, rnum1=None, rnum2=None, row1=None, row2=None):
		"""add row2 to row1 and return nothing"""
		assert rnum1 is not None and (rnum2 is not None or row2 is not None), "index must be provided"		
		m = self.getMatrix()
		row1 = m[rnum1]
		if rnum2 is not None:
			row2 = m[rnum2]
		for i in range(len(row1)):
			row1[i] -= row2[i]
		m[rnum1] = row1
		self.setMatrix(m)
	
	
	# tools
	
	def remColumn(self, var):
		m = self.getMatrix()
		new_m = m[:]
		keys = self.keys
		index = keys.index(var)
		for i in range(len(m)):
			del new_m[i][index]
		self.setMatrix(m)
	
	def makeEquation(self, rnum):
		"""returns the str form of the equation"""
		m = self.getMatrix()
		row = m[rnum]
		keys = self.getKeys()
		out = ""
		for i in range(len(keys)):
			out += str(row[i])+keys[i] if row[i] != 0 else ""
			out += " "
		out += "= "
		out += str(row[-1])
		return out
			
	
	def __str__(self):
		m = self.getMatrix()
		out = ""
		for e in m:
			out += str(e) + "\n"
		out = out[:-1]
		return out
	

def solveSystems(sys):
	"""
	:result: Takes in a system of simultaneous linear equations and solves them
	> In an n by n+1 matrix, the last column will be the value of the equations.
	Now, to achieve this, we can implement a loop that goes through each row and
	one after the other, row by row and column by column.
	This way, it will get a "pivot" that shall be the intersection of rows and
	columns.
	The aim of this program shall be to get the pivot and make the values of the
	other rows in the same column equal to 0, via row operations.
	"""
	matrix = sys.getMatrix()
	if len(matrix) == 2:
		# get the first elements of both matrices
		n1 = matrix[0][0]
		n2 = matrix[1][0]
		cm = n1*n2  # this is the common multiple. ideally it should be the lcm
		# make the first term of both rows the same
		sys.multRow(0, cm/n1)
		sys.multRow(1, cm/n2)
		print("multiplied rows")
		print(sys)
		# subtract one row from another
		sys.subRow(rnum1=0, rnum2=1)
		print("subtracted rows")
		print(sys)
		sys.multRow(0, 1/sys.getRow(0)[1])
		print(sys)
		print(sys.makeEquation(0))
		sol1 = sys.getRow(0)[-1]
		toSolve = []
		row2 = sys.getRow(1)
		k = self.getKeys()
		for i in range(len(keys)):
			if i != 1:
				toAppend = str(row2[i])+keys[i]
				toSolve.append(toAppend)
			else:
				toSolve.append(str(row2[i]*sol1))
			toSolve.append(row2[-1])
		
		
	



