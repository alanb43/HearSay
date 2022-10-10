# This is a simple demo of a pretrained model

from transformers import pipeline

clf = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')

labels = ['sports player trade', 'sports player injury', 'sports player biography']

print("Ready for queries.")

while True:
    phrase = input()
    print(clf(phrase, labels))
