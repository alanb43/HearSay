from transformers import TrainingArguments, Trainer, AutoTokenizer, DataCollatorWithPadding, AutoModelForSequenceClassification
import numpy as np
from datasets import load_metric, load_dataset
import torch

def compute_metrics(eval_pred):
   load_accuracy = load_metric("accuracy")
   load_f1 = load_metric("f1")
  
   logits, labels = eval_pred
   predictions = np.argmax(logits, axis=-1)
   accuracy = load_accuracy.compute(predictions=predictions, references=labels)["accuracy"]
   f1 = load_f1.compute(predictions=predictions, references=labels)["f1"]
   return {"accuracy": accuracy, "f1": f1}

def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True)

dataset = load_dataset("json", data_files="dataset.json")["train"]

tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")
model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment-latest")

tokenized_train = dataset.map(preprocess_function, batched=True)



repo_name = "finetune-sentiment-model-players-teams"

training_args = TrainingArguments(
   label_names = [0, 1, 2],
   output_dir=repo_name,
   learning_rate=2e-5,
   per_device_train_batch_size=16,
   per_device_eval_batch_size=16,
   num_train_epochs=2,
   weight_decay=0.01,
   save_strategy="epoch",
   push_to_hub=False,
)
 
trainer = Trainer(
   model=model,
   args=training_args,
   train_dataset=tokenized_train,
   eval_dataset=tokenized_train,
   tokenizer=tokenizer,
   compute_metrics=compute_metrics,
)

trainer.train()