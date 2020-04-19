import os, string, re, sys
import json
from _collections import defaultdict

file_read = open(sys.argv[1], 'r')
json_data = json.load(file_read)


print("\nWords not in spam")
for key,val in json_data['prob_word_given_spam']:
	if(key in spamDict) :
		continue
	else:
		print(key + "\n")

print("\nWords not in spam")
for key,val in json_data['prob_word_given_ham']:
	if(key in hamDict) :
		continue
	else:
		print(key + "\n")

#for key,val in json_data.iteritems():
#	for k,v in val.items():

