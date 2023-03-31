# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 14:14:34 2023

@author: ishank

Contains the solver programs and algorithms
"""

import math
from fractions import Fraction
from classes import Term, Expression, Equation


def linearSolve(eq: Equation):
	"""solves linear equations
	implements the following steps:
	-> isolates the variables on the LHS or RHS
	-> divides the coef to get value of the variables
	note: only linear equations with single variables can be solved by
	this program
	STATUS: WORKS
	"""
	simpled = eq.isolate()
	div_by = simpled.getExpr1().getTerms()[0].getVal()
	#print(div_by)
	simpled.divBy(Term(str(div_by)))
	return simpled


def checkEquaForm(expr):
	if len(expr.getTerms()) > 3:
		return False
	if expr.getDegree() > 2:
		return False
	return True
	
def quadMath(a, b, c):
	"""
	takes in a, b and c and returns two numbers that solve the
	quadratic equation
	The logic behind this:
	ax2 + bx + c
	can be solved by the identities (a+b)2 and (a-b)2
	-> we need to find two numbers that add up to b and multiply to form a*c
	"""
	sq_sum = b**2 - 2*a*c
	#print("sq_sum", sq_sum)
	diff_sq = sq_sum - 2*a*c
	#print("diff_sq", diff_sq)
	diff = diff_sq**0.5
	#print("diff", diff)
	# Now that we have the sum and the diff, we can solve the system of equations
	p = (b+diff)/2
	q = b-p
	return int(p), int(q)
	

def quadSolve(eq, steps=False):
	"""
	solves quadratic equations
	This one requires some more steps
	-> Make RHS 0
	-> determine term with power 2 and constant
	-> form relation between a and b
	    ax2 + (a+b)x + b
	-> get values of a and b using (a+b)2 = a2 + b2 + 2ab
	    and (a-b)2 = a2 + b2 -2ab
	-> factorise
	-> take each factor as 0 to get linear equation
	-> get two solutions
	"""
	expr2 = eq.getExpr2()
	for i in expr2.getTerms():
		i.swapSign()
		eq.addTo(i)
	expr1 = eq.getExpr1()
	expr2 = eq.getExpr2()
	print("After simplification, expr1, expr2", expr1, expr2)
	expr1.sort()
	eq.setExpr1(expr1)
	assert checkEquaForm(expr1), "Expr1 is not of the proper form" + str(expr1)
	# Equation is now ready for solving;
	# It is in ax2 + bx + c form
	terms = expr1.getTerms()
	a = int(terms[0].getVal())
	b = int(terms[1].getVal())
	c = int(terms[2].getVal())
	#print("abc", a, b, c)
	p, q = quadMath(a, b, c)
	#print("p, q", p, q)
	if steps:
		print(eq)
		print("{}x2 + ({} + {})x + {}".format(a, p, q, c))
	
	hcf1, hcf2 = math.gcd(a, p), math.gcd(q, c)
	if sig(str(a)) == "-":
		hcf1 = int("-"+str(hcf1))
	if sig(str(q)) == "-":
		hcf2 = int("-"+str(hcf2))
	if steps:
		print("{}x2 + {}x + {}x + {}".format(a, p, q, c))
		print("{}x({}x + {}) + {}({}x + {})".format(hcf1, a/hcf1, p/hcf1, hcf2, q/hcf2, c/hcf2))	
		print("({}x + {})({}x + {})".format(hcf1, hcf2, a/hcf1, c/hcf2))
	
	solns = Fraction(-hcf2/hcf1), Fraction(-c*hcf1/(a*hcf2))
	print("Solutions of Quadratic Equation")
	return solns



def solver(eq, steps=False):
	"""solves the equation given"""
	# first get the degree of the equation and solve accordingly
	degr = eq.getDegree()
	if degr == 1:
		soln = linearSolve(eq)
		#if len(soln.getExpr1().getTerms()) == 1:
			#print("Therefore, solution of the given equation is:")
			#print(soln.getExpr1().getTerms()[0].getOnlyVars()+" = "+str(soln.getExpr2().getTerms()[0]))
		print("Solution of linear equation:")
		print(soln.wop())
		return soln
	elif degr == 2:
		solns = quadSolve(eq, steps)
		if steps:
			return str(solns[0]), str(solns[1])
		else:
			return solns
	else:
		raise ValueError("only equations of degrees 1 or 2 can be solved")


def addMultiple(terms, expr):
	for i in terms:
		print("BF ADD", str(i), str(expr))
		expr.addTo(i)
		print("AF ADD", str(i), str(expr))
	return expr


