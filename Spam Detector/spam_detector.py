import sys
import re

train_data_path = sys.argv[1]
test_data_path = sys.argv[2]
output_data_path = sys.argv[3]

spams = []
hams = []
tests = []
clean_tests = []
spam_words = {}
ham_words = {}

train_file = open(train_data_path, "r")
for line in train_file:
    split_line = line.split('\t')
    if split_line[0] == 'ham':
        hams.extend(re.sub(r'[\W+]', ' ', split_line[1]).split(' '))
    else:
        spams.extend(re.sub(r'[\W+]', ' ', split_line[1]).split(' '))
train_file.close()

test_file = open(test_data_path, "r")
for line in test_file:
    tests.append(line)
    clean_tests.append(re.sub(r'[\W+]', ' ', line))
test_file.close()

for word in hams:
    if word in ham_words:
        ham_words[word] += 1
    else:
        ham_words[word] = 1
for word in spams:
    if word in spam_words:
        spam_words[word] += 1
    else:
        spam_words[word] = 1


num_vocabulary = len(spams + hams)
p_ham = len(hams) / num_vocabulary
p_spam = len(spams) / num_vocabulary


def spam_word_possibility(wrd):
    num_spams = len(spams)
    if wrd in spam_words:
        return (spam_words[word] + 1) / (num_spams + num_vocabulary)
    else:
        return 1 / (num_spams + num_vocabulary)


def spam_possibility(sentence):
    words = sentence.split(' ')
    result = p_spam
    for i in range(len(words)):
        result *= spam_word_possibility(words[i])
    return p_spam * result


def ham_word_possibility(wrd):
    num_hams = len(hams)
    if wrd in ham_words:
        return (ham_words[word] + 1) / (num_hams + num_vocabulary)
    else:
        return 1 / (num_hams + num_vocabulary)


def ham_possibility(sentence):
    words = sentence.split(' ')
    result = p_ham
    for i in range(len(words)):
        result *= ham_word_possibility(words[i])
    return result


file = open(output_data_path, 'w')
for j in range(len(tests)):
    if ham_possibility(clean_tests[j]) > spam_possibility(clean_tests[j]):
        file.write('ham\t' + tests[j])
    else:
        file.write('spam\t' + tests[j])
file.close()
