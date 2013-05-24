# -*- coding: utf-8 -*-


_sing_rules = [lambda w: w[-3:] == 'ies' and w[:-3] + 'y',
               lambda w: w[-4:] == 'ives' and w[:-4] + 'ife',
               lambda w: w[-3:] == 'ves' and w[:-3] + 'f',
               lambda w: w[-2:] == 'es' and w[:-2],
               lambda w: w[-1:] == 's' and w[:-1],
               lambda w: w,
              ]
#
#
def Singularize(word):
	"""
	Singularize(word) -> Return the singular form of a word [english], it does
					not work with irregular plurals
	"""
	global _sing_rules

	word = word.strip()
	singword = ''
	for f in _sing_rules:
		if f(word):
			singword = f(word)
			break

	return singword