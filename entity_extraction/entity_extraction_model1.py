from transformers import AutoModelForTokenClassification, AutoTokenizer, pipeline

model_dir = './frankie_trained_model'

nlp = pipeline('ner', model=model_dir, tokenizer=model_dir, aggregation_strategy="simple")

sentence =" "
while (sentence != "DONE"):
    sentence = input("Enter a sentence\n")
    print(nlp(sentence))
