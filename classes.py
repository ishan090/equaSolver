# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:03:52 2023

@author: ishank

Contains all the Classes

"""


from string import ascii_letters


class Term():
	def __init__(self, term):
		"""term is a string"""
		#term = term.replace(" ", "")
		#print("TERM TO BE PARSED", term)
		var = ""
		num = ""
		sign = term
		for i, j in enumerate(term):
			if isNotSign(j):
				sign = term[:i]
				num = term[i:]
				break
		#print("!", repr(sign), repr(num))
		for k, l in enumerate(num):
			if isVar(l):
				#print("*", l, k)
				var = num[k:]
				num = num[:k]
				break
		#print("!!", num, var)
		sign = sig(sign)
		#num = num.split('x')
		#print("-->", num)
		if num == "" and var == "":
			coef = 0
		else:
			coef = makeFloat(num)
		#print("@", sign, coef, var)
		var_s = getVars(var[::-1])
		self.sign = sign
		self.coef = coef
		self.var_s = var_s
	
	# getters
	def getCoef(self):
		return self.coef
	def getSign(self):
		return self.sign
	def getVal(self):
		return float(self.getSign()+str(self.getCoef()))
	def getVars(self):
		return self.var_s
	def getLitCoef(self):
		var_s = self.getVars()
		var = ""
		for i in var_s.keys():
			var += i+str(var_s[i])
		return var
	def getWithoutSign(self):
		return str(self.getCoef())+self.getLitCoef()
	def wop(self):
		v = "".join(list(self.getVars().keys()))
		return v

	def wopAll(self):
		return self.getSign()+str(self.getCoef())+self.wop()
	
	# setters
	def setCoef(self, coef):
		self.coef = float(coef)
	def setVars(self, var):
		self.var_s = var
	def setSign(self, sign):
		self.sign = sign
	
	# operations
	# ADD TERMS
	def addTerms(self, term):
		if self.getVars() == term.getVars():
			coef = self.getVal()+term.getVal()
		else:
			raise ValueError("Terms aren't like terms")
		return Term(str(coef)+self.getLitCoef())
	

	# MULTIPLY TERMS
	def multTerms(self, ter1, ter2):
		new_coef = ter1.getCoef()*ter2.getCoef()
		vars1 = ter1.getVars()
		vars2 = ter2.getVars()
		for var in vars2:
			vars1[var] = vars1.get(var, 0) + vars2[var]
		new_sign = sig(ter1.getSign()+ter2.getSign())
		ter1.setSign(new_sign)
		ter1.setCoef(new_coef)
		ter1.setVars(vars1)
		return ter1

	# DIVIDE TERMS
	def divTerms(self, ter1, ter2):
		new_coef = ter1.getCoef()/ter2.getCoef()
		vars1 = ter1.getVars()
		vars2 = ter2.getVars()
		for var in vars2:
			vars1[var] = vars1.get(var, 0) - vars2[var]
		new_sign = sig(ter1.getSign()+ter2.getSign())
		ter1.setSign(new_sign)
		ter1.setCoef(new_coef)
		ter1.setVars(vars1)
		return ter1


	# tools
	def power(self):
		var = self.getLitCoef()
		if var == "":
			return 1
		m = max(self.getVars().values())
		return m
		
	def sig(self, signs):
		"""signs is a string, returns str"""
		return ['+', '-'][signs.count('-') % 2]

	def swapSign(self):
		cur_sign = self.getSign()
		newSign = sig(cur_sign+"-")
		self.setSign(newSign)
	
	def __str__(self):
		return self.getSign()+str(self.getCoef())+self.getLitCoef()
		


# CLASS EXPRESSION
class Expression():
	def __init__(self, terms, terlist=None):
		if terlist is not None:
			new_terms = terlist
		else:
			new_terms = self.parse(terms)
		self.terms = new_terms
	
	def parse(self, terms):
		new_terms = []
		#print("%"*25)
		#print(len(terms.split()))
		t = 0
		#print("TERMS PARSE SPLIT", terms.split())
		for i, j in enumerate(terms.split()):
			#print("ij", i, j)
			if isTerm(j):
				#print("t before", t)
				#print("j", j, "is a term")
				signs = sig(terms.split()[t:i])
				#print("t", t, "i", i, terms.split())
				#print("signs gathered", terms.split()[t:i])
				term = signs+j
				new_terms.append(Term(term))
				t = i+1
				#print("t after", t)
		#print("%"*25)
		#print(len(new_terms))
		return new_terms

	# getters
	def getTerms(self):
		return self.terms
	def getPrintedTerms(self):
		return [str(i) for i in self.terms]
	def getVars(self):
		vs = []
		for i in self.getTerms():
			vs.append(i.getLitCoef())
		return vs
	
	# setters
	def setTerms(self, terms):
		"""terms is a list of terms"""
		self.terms = terms
	
	# operations
	# ADD
	def addTo(self, term):
		"""term is a Term"""
		#print("Add function attempting to add", self.getTerms(), "and", term)
		allVars = self.getVars()
		terms = self.getTerms()
		#print("EXPR.ADDTO()", term, type(term), str(self))
		#print("-> Terms", str(self))
		termVars = term.getLitCoef()
		found = False
		for i in range(len(self.getTerms())):
			if termVars == allVars[i]:
				found = True
				#print("like term found", i, terms[i] )
				#print("term[i] BF", terms[i])
				terms[i] = term.addTerms(terms[i])
				#print("term[i] AF", terms[i])
				break
		if not found:  # then add as a separate term
			terms.append(term)
		terms = [i for i in terms if i.getCoef() != 0]
		if terms == []:
			terms = [Term("0")]
		self.setTerms(terms)

	# MULTIPLY
	def multBy(self, term):
		terms = self.terms
		for i in range(len(terms)):
			terms[i] = terms[i].multTerms(terms[i], term)
		self.setTerms(terms)

	# DIVIDE
	def divBy(self, term):
		terms = self.terms
		#print("EXPR.divBy", str(terms), "TERM", term)
		for i in range(len(terms)):
			terms[i] = terms[i].divTerms(terms[i], term)
		self.setTerms(terms)


	# tools
	def getDegree(self):
		degree = 1
		for i in self.getTerms():
			if i.power() > degree:
				degree = i.power()
		return degree
	
	def wop(self):
		out = ""
		terms = self.getTerms()
		#print("TERMS WOP", terms)
		out += terms[0].wopAll()+" "
		for i in terms[1:]:
			out += i.getSign()+" "+str(i.getCoef())+i.wop()+" "
		return out

	def sort(self):
		sorted_list = [Term("0"), Term("0"), Term("0")]
		for i in self.getTerms():
			#print("Term to be sorted i", i)
			if i.power() == 2:
				#print("Term i", i, "has power 2")
				sorted_list[0] = i
			elif isCons(str(i)):
				#print("Term i", i, "is a constant")
				sorted_list[2] = i
			else:
				#print("Term i", i, "is not a constant")
				sorted_list[1] = i
		self.setTerms(sorted_list)
			
	
	def __str__(self):
		out = ""
		terms = self.getTerms()
		#print("-")
		#print("TERMS WOP", terms)
		out += str(terms[0])+" "
		for i in terms[1:]:
			out += i.getSign()+" "+i.getWithoutSign()+" "
		return out




class Equation():
	def __init__(self, equa):
		"""
		equa is a string
		"""
		expr1 = equa[:equa.index("=")]
		expr2 = equa[equa.index("=")+1:]
		#print("EQ INIT 1, 2", repr(expr1), repr(expr2))
		self.expr1 = Expression(expr1)
		expre2 = Expression(expr2)
		#print("EXPRE2", expre2)
		self.expr2 = expre2
	
	# getters
	def getExpr1(self):
		return self.expr1
	def getExpr2(self):
		return self.expr2
	
	# setters
	def setExpr1(self, expr):
		self.expr1 = expr
	def setExpr2(self, expr):
		self.expr2 = expr

	# operations
	# ADD
	def addTo(self, term):
		#print("Trying to add", term, "to", self.getExpr2())
		# retrieve
		expr1, expr2 = self.getExpr1(), self.getExpr2()
		#print("EQ BF ADD CHANGE", repr(expr1), repr(expr2))
		# edit
		expr1.addTo(term)
		#print("EQ ADD AF CH1", repr(expr1))
		expr2.addTo(term)
		#print("EQ ADD AF CH2", expr2)
		# replace
		self.setExpr1(expr1)
		self.setExpr2(expr2)
	
	# MULTPLY
	def multBy(self, term):
		# retrieve
		expr1, expr2 = self.getExpr1(), self.getExpr2()
		# edit
		expr1.multBy(term)
		expr2.multBy(term)
		# replace
		self.setExpr1(expr1)
		self.setExpr2(expr2)
	
	# DIVIDE
	def divBy(self, term):
		# retrieve
		expr1, expr2 = self.getExpr1(), self.getExpr2()
		# edit
		expr1.divBy(term)
		expr2.divBy(term)
		# replace
		self.setExpr1(expr1)
		self.setExpr2(expr2)

	
	# tools
	def getDegree(self):
		d1 = self.getExpr1().getDegree()
		d2 = self.getExpr2().getDegree()
		return max(d1, d2)
	
	def wop(self):
		expr1, expr2 = self.getExpr1(), self.getExpr2()
		out = expr1.wop()+" = "+expr2.wop()
		return out
	
	def getVarsMatrix(self):
		eq = self.isolate()
		expr1 = eq.getExpr1()
		matrix_form = {}
		for i in expr1.getTerms():
			matrix_form[i.getLitCoef()] = i.getVal()
		matrix_form[""] = eq.getExpr2().getTerms()[0].getVal()
		return matrix_form

	def getTerms(self):
		eq = self.isolate()
		print("GETTerms Iso", eq)
		e1 = eq.getExpr1()
		return e1.getTerms()

	def isolate(self):
		#print("ISOL START")
		ans = Equation(str(self))
		#print("ANS", ans)
		expr1 = self.getExpr1()
		expr2 = self.getExpr2()
		print("EXPR1, EXPR2", expr1, expr2)
		for i in expr1.getTerms():
			print("EXPR1 i", i)
			if isCons(str(i)):
				i.swapSign()
				print("LINSOL TOADD", i)
				ans.addTo(i)
				print("ans", ans)
		#print("ISOL expr2", expr2)
		print("EXPR2.GETTERMS", expr2.getTerms())
		for j in expr2.getTerms():
			print("EXPR2 j", j, "isCons", isCons(str(j)))
			if not isCons(str(j)):
				print("TERM", j, "IS A VAR")
				j.swapSign()
				ans.addTo(j)
	return ans


	def __str__(self):
		expr1 = str(self.getExpr1())
		expr2 = str(self.getExpr2())
		return expr1 + " = " + expr2
		


def isTerm(term):
	for i in term:
		if i not in "+-":
			return True
	return False

def sig(terms):
	"""terms is a string, returns str"""
	return ['+', '-'][terms.count('-') % 2]



def makeFloat(x):
	if x == "":
		return 1.0
	return float(x)

def getVars(var):
	v = 0
	var_s = {}
	for i, j in enumerate(var):
		if isVar(j):
			var_s[j] = var_s.get(j, 0) + makeFloat(var[v:i][::-1])
			v = i+1
	return var_s


def isCons(term):
	"""
	checks if a term is a constant
	takes string and returns bool
	returns true if term is a float (with sign)
	"""
	try:
		float(term)
		#print("TERM ISCOS", term)
		return True
	except:
		return False

#print(isCons("--34"))


def ValidTerm(term):
	for i in term:
		if i not in "+-":
			return True
	return False

def isVar(v):
	return v in ascii_letters
def isNum(n):
	return n in "0123456789"
def isNotSign(s):
	return s not in "+-"

def makeFloat1(x):
	if x == "":
		return 1.0
	return float(x)








