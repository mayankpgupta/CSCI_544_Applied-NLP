import os, string, re, sys
import json
from _collections import defaultdict

correct_spam = 0
correct_ham = 0
spam = 0
ham = 0
actual_spam = 0
actual_ham = 0


def calc_fscore(p,r):
	fscore = (2*p*r)/(p+r)
	return fscore

file_read = open(sys.argv[1], 'r')
lines  = file_read.readlines()
for line in lines:
	#print(line.strip())
	text = line.split("\t")
	
	if text[0] == 'spam':
		if 'spam' in text[1]:
			correct_spam +=1
		spam +=1
	elif text[0] == 'ham':
		if 'ham' in text[1]:
			correct_ham +=1
		ham +=1
	if text[0] == 'spam' or text[0] == 'ham':
		if 'spam' in text[1]:
			actual_spam +=1
		elif 'ham' in text[1]:
			actual_ham +=1

precision_spam = correct_spam/spam
precision_ham = correct_ham/ham
recall_spam = correct_spam/actual_spam
recall_ham = correct_ham/actual_ham

fscore_spam = calc_fscore(precision_spam,recall_spam)
fscore_ham = calc_fscore(precision_ham,recall_ham)

print("\n Precision (spam) : " + str(precision_spam))
print("\n Precision (ham) : " + str(precision_ham))
print("\n Recall (spam) : " + str(recall_spam))
print("\n Recall (ham) : " + str(recall_ham))
print("\n FScore (spam) : " + str(fscore_spam))
print("\n FScore (ham) : " + str(fscore_ham))