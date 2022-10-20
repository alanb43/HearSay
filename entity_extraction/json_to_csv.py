import json
import csv

def label_data(data):
    dictionary = {"tokens": [], "tags": []}
    tokens = []
    tags = []

    for sentence in data:
        seperated_words = sentence.split(" ")

        words = []
        poss = []
        tagss = []

        i = 0
        while i < len(seperated_words):
            word = seperated_words[i]

            if (word[0] == '['):
                chunk = word[1:]
                j = i
                while (seperated_words[j].find(']') == -1):
                    j = j + 1

                    if (j != i):
                        chunk = chunk + " " + seperated_words[j]

                words.append(chunk.split(']')[0])

                if (chunk.split(']')[1][1:3] == "pe" or chunk.split(']')[1][1:3] == "pl"):
                    tagss.append("PER")
                else:
                    tagss.append("TEAM")
                i = j + 1

            else:
                words.append(word)
                tagss.append("O")
                i = i + 1
        tokens.append(words)
        tags.append(tagss)

    dictionary["tokens"] = tokens
    dictionary["tags"] = tags

    return dictionary

with open("ner_train.json", 'r') as file:
    file = json.load(file)
    dictionary = label_data(file)

with open('train-ner.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=',')

    header = ['tokens', 'tags']

    writer.writerow(header)

    for i in range(len(dictionary['tokens'])):
        writer.writerow([dictionary['tokens'][i], dictionary['tags'][i]])