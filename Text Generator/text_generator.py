from random import choice

file = open('speech.txt',mode='r', encoding='utf-8')
speech = file.read()
file.close()

words = speech.split(' ')
dict = {}
starters = []

for i in range(len(words) - 1):
    if '.' in words[i]:
        starters.append(words[i + 1])
    if words[i] in dict.keys():
        if words[i + 1] in dict[words[i]]:
            dict[words[i]][words[i + 1]] += 1
        else:
            dict[words[i]][words[i + 1]] = 1
    else:
        dict[words[i]] = {words[i + 1]: 1}
        

def find_suggestion(str):
    if str in dict:
        array = []
        after_words = dict[str]
        for word in after_words:
            array.append(after_words[word])
        array.sort(reverse= True)
        result = set()
        for word in after_words:
            if after_words[word] == array[0] or after_words[word] == array[1] or after_words[word] == array[2]:
                result.add(word)
        return list(result)
    else:
        return list()


def random_sentence():
    sentence = choice(starters) + ' '
    while True:
        suggestions = find_suggestion(sentence.split().pop())
        word = choice(suggestions)
        sentence += word + ' '
        if '.' in word:
            break
    return sentence


print(random_sentence())
