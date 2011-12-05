def get_permutations(word, group_dict): 
	if word: 
		for first in group_dict[word[0]]: 
			for rest in get_permutations(word[1 : ], group_dict): 
				yield first + rest 
	else: 
		yield "" 

def count_permutations(word, group_dict): 
	if word: 
		total = 1 
		for letter in word: 
			total *= len(group_dict[letter]) 
		return total 
	else: 
		return 0 


gdef = [['x', 'X', 'm'], ['Y', 'V', 'v'], ['X', 'I', 'l'], ['y', 'k', 't'], ['X', 'i', 'x'], ['x', 'y', 'Y'], ['q', 'a', 'A'], ['Y', 'r', 't'], ['I', 'l', 'f'], ['x', 'a', 'q'], ['X', 'x', 'k'], ['c', 'u', 'N']]
group_def = "crb azk ht" 

group_dict = {} 
for group in gdef:
	for letter in group: 
		group_dict[letter] = group 

word = u"xYXYXXqYIxXN" 

print "There are %d permutations." % count_permutations(word, group_dict) 
print 

for perm in get_permutations(word, group_dict): 
	print perm 