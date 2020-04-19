import os, string, re, sys
import json
from _collections import defaultdict


file_read = open('nbmodel.txt', 'r', encoding='latin1')
file_write = open('nboutput.txt','w')
json_data = json.load(file_read)
prob = {}
prob_spam = json_data["spam"]
prob_ham = json_data["ham"]
prob_word_spam = json_data["word|spam"]
prob_word_ham = json_data["word|ham"]


files_list = []

for dirpath, dirnames, files in os.walk(sys.argv[1]):
    for file in files:
    	if '.txt' in file:
    		if 'spam' in dirpath:
    			files_list.append(os.path.join(dirpath, file))
    		if 'ham' in dirpath:
    			files_list.append(os.path.join(dirpath, file))

for file in files_list:
	spam_prob_words = prob_spam
	ham_prob_words = prob_ham
	f = open(file, 'r', encoding="latin1")
	for x in f :
		text = x.lower()
		words = text.strip().split()
		for w in words:
			if w in prob_word_spam:
				spam_prob_words += prob_word_spam[w]
			if w in prob_word_ham:
				ham_prob_words += prob_word_ham[w]
	head, tail = os.path.split(file)
	if(spam_prob_words > ham_prob_words):
		file_write.write('\nspam\t' + str(tail))
	else:
		file_write.write('\nham\t' + str(tail))
