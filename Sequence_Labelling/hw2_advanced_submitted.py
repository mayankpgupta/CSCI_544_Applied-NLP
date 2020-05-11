from collections import namedtuple
import csv
import glob
import os
import sys
import time
import pycrfsuite

startTime = time.time()

def token_Bigrams(tokens):
    bigrams = list()
    if(len(tokens) > 1):
        for i in range(0,(len(tokens) - 1)):
            bigrams.append(tokens[i] + "_" + tokens[i+1])
    return bigrams


def token_Trigrams(tokens):
	trigrams = list()
	if(len(tokens)>1):
		for i in range(0,(len(tokens)-2)):
			trigrams.append(tokens[i] + "_" + tokens[i+1] + "_" + tokens[i+2])
	return trigrams


def get_utterances_from_file(dialog_csv_file):
    """Returns a list of DialogUtterances from an open file."""
    reader = csv.DictReader(dialog_csv_file)
    return [_dict_to_dialog_utterance(du_dict) for du_dict in reader]

def get_utterances_from_filename(dialog_csv_filename):
    """Returns a list of DialogUtterances from an unopened filename."""
    with open(dialog_csv_filename, "r") as dialog_csv_file:
        return get_utterances_from_file(dialog_csv_file)

def get_data(data_dir):
    """Generates lists of utterances from each dialog file.

    To get a list of all dialogs call list(get_data(data_dir)).
    data_dir - a dir with csv files containing dialogs"""
    dialog_filenames = sorted(glob.glob(os.path.join(data_dir, "*.csv")))
    for dialog_filename in dialog_filenames:
        #print(dialog_filename)
        yield get_utterances_from_filename(dialog_filename)

DialogUtterance = namedtuple(
    "DialogUtterance", ("act_tag", "speaker", "pos", "text"))

DialogUtterance.__doc__ = """\
An utterance in a dialog. Empty utterances are None.

act_tag - the dialog act associated with this utterance
speaker - which speaker made this utterance
pos - a list of PosTag objects (token and POS)
text - the text of the utterance with only a little bit of cleaning"""

PosTag = namedtuple("PosTag", ("token", "pos"))

PosTag.__doc__ = """\
A token and its part-of-speech tag.

token - the token
pos - the part-of-speech tag"""


def obtain_features(sequences):
	feature_vector = []
	dialogue_act_labels = []
	for utterances in sequences:
		beginning = 1
		for u in utterances:
			tokensForFeature = []
			token_list = []
			pos_list = []
			vector_temp = []
			text_list = []
			token_position = []
			if(beginning == 1):
				vector_temp.append('0')
				vector_temp.append('BEGINNING')
				beginning = 0
				prev_speaker = u.speaker
			else :
				if (prev_speaker == u.speaker):
					vector_temp.append('0')
				else :
					vector_temp.append('1')
					prev_speaker = u.speaker
				vector_temp.append('NOT_BEGINNING')
			if (u.pos is not None):
				position = 0
				for x in u.pos:
					position += 1
					token_list.append(x.token)
					pos_list.append(x.pos)
					token_position.append(position)
					tokensForFeature.append(x.token)
				for i in range(0, len(token_list)):
					vector_temp.append(token_list[i] + " " + str(token_position[i]))
				for p in pos_list:
					vector_temp.append(p)
				bigrams = token_Bigrams(tokensForFeature)
				for b in bigrams:
					vector_temp.append(b)
				trigrams = token_Trigrams(tokensForFeature)
				for tri in trigrams:
					vector_temp.append(tri)
			else:
				vector_temp.append("NONE")
				vector_temp.append("NONE")
			if (position<4):
				vector_temp.append('TOKEN_COUNT_LESS')
			else:
				vector_temp.append('TOKEN_COUNT_MORE')

			for t in u.text.split():
				vector_temp.append("TEXT_"+ t)
			feature_vector.append(vector_temp)
			if(u.act_tag is not None):
				dialogue_act_labels.append(u.act_tag)
	return feature_vector, dialogue_act_labels

        
        

def _dict_to_dialog_utterance(du_dict):
    """Private method for converting a dict to a DialogUtterance."""

    # Remove anything with 
    for k, v in du_dict.items():
        if len(v.strip()) == 0:
            du_dict[k] = None

    # Extract tokens and POS tags
    if du_dict["pos"]:
        du_dict["pos"] = [
            PosTag(*token_pos_pair.split("/"))
            for token_pos_pair in du_dict["pos"].split()]
    return DialogUtterance(**du_dict)

train_data = get_data(sys.argv[1])
train_data = list(train_data)

x_data, y_data = obtain_features(train_data)

test_data = get_data(sys.argv[2])
test_data = list(test_data)
x_test_data, y_actual_data = obtain_features(test_data)


crf_trainer = pycrfsuite.Trainer(verbose = False)
crf_trainer.append(x_data,y_data)

crf_trainer.set_params({
 'c1': 1.0,
 'c2': 1e-3,
 'max_iterations': 50,
 'feature.possible_transitions': True
 })

crf_trainer.train('advanced_model')

crf_tagger = pycrfsuite.Tagger()
crf_tagger.open('advanced_model')

predicted_act_tag = crf_tagger.tag(x_test_data)
count = 0
file = open(sys.argv[3], 'w')
for i in range(0, len(x_test_data)):
	if(x_test_data[i][1] is 'BEGINNING') and (count < len(test_data)):
		if (count != 0):
			file.write("\n")
		count += 1
		file.write(predicted_act_tag[i] + "\n")
	else:
		file.write(predicted_act_tag[i] + "\n")
file.close()
value = 0
for p in range(0, len(x_test_data)):
	if y_actual_data[p] == predicted_act_tag[p]:
		value += 1
	p += 1
accuracy = float(value/len(x_test_data))
print("Accuracy : " + str(accuracy))
endTime = time.time()
print("Duration : " + str(endTime - startTime))