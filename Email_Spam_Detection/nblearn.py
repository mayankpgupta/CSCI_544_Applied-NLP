import os, string, re, sys
import json
import math
from _collections import defaultdict

spamDict = {}
hamDict = {}
vocabularyDict = {}
total_words = 0
spam_count = 0
ham_count = 0

def store_in_dict(dict_name, email):
	global total_words
	text = email.lower()
	words = text.strip().split(" ")
	for w in words :
		total_words += 1
		if(w not in dict_name):
			dict_name[w] = 1
		else:
			dict_name[w] +=1
		if(w not in vocabularyDict):
			vocabularyDict[w] = 1

def cal_spam_prob(w):
	word_count = 0
	if(w in spamDict):
		word_count = spamDict[w] + 1
	else:
		word_count += 1
	prob = float(word_count/(spam_word_count + len(vocabularyDict)))
	return prob
	

def cal_ham_prob(w):
	word_count = 0
	if(w in hamDict):
		word_count = hamDict[w] + 1
	else:
		word_count += 1
	prob = float(word_count/(ham_word_count + len(vocabularyDict)))
	return prob

files_list = []

for dirpath, dirnames, files in os.walk(sys.argv[1]):
    for file in files:
    	if '.txt' in file:
    		if 'spam' in file:
    			files_list.append(os.path.join(dirpath, file))
    		if 'ham' in file:
    			files_list.append(os.path.join(dirpath, file))

for file in files_list:
	f = open(file, 'r', encoding="latin1")
	head, tail = os.path.split(file)
	for x in f:
		if 'spam' in tail:
			store_in_dict(spamDict, x)
		if 'ham' in tail:
			store_in_dict(hamDict, x)

spam_word_count = 0
ham_word_count = 0

for x,y in spamDict.items():
	spam_word_count += y

for x,y in hamDict.items():
	ham_word_count += y

print("\n\nHam count " + str(ham_word_count))
print("\nSpam count " + str(spam_word_count))

prob1 = {}

prob_spam = float(spam_word_count/total_words)
prob_ham = float(ham_word_count/total_words)

prob1["spam"] = math.log2(prob_spam)
prob1["ham"] = math.log2(prob_ham)

prob1_spam = {}
prob1_ham = {}

for w in vocabularyDict:
	val1 = cal_spam_prob(w)
	val2 = cal_ham_prob(w)
	prob1_spam[w] = math.log2(val1)
	prob1_ham[w] = math.log2(val2)

prob1["word|spam"] = prob1_spam
prob1["word|ham"] = prob1_ham

json_obj = json.dumps(prob1)
file1 = open("nbmodel.txt",'w')
file1.write(json_obj)
file1.close()



