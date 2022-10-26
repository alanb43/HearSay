# Trained and tested basic transformer NER model that is in Jaseci

I just copied the tfm_ner.jac file from the intro assignment

## Steps to train and test

1. Activate environment with jaseci installed

2. Enter jaseci shell
```
jsctl
```
3. Load the module in the jaseci shell
```
jaseci > actions load module jaseci_ai_kit.tfm_ner
```

4. Train the model

```
jaseci > jac run tfm_ner.jac -walk train -ctx "{\"train_file\": \"ner_train.json\"}"
```

5. Test inference

```
jaseci > jac run tfm_ner.jac -walk infer
```

