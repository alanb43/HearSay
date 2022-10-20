---
tags:
- autotrain
- token-classification
language:
- en
widget:
- text: "I love AutoTrain 🤗"
datasets:
- frankielizcano/autotrain-data-train_player_org
co2_eq_emissions:
  emissions: 0.9406671240037067
---

# Model Trained Using AutoTrain

- Problem type: Entity Extraction
- Model ID: 1810562486
- CO2 Emissions (in grams): 0.9407

## Validation Metrics

- Loss: 0.171
- Accuracy: 0.990
- Precision: 0.938
- Recall: 0.938
- F1: 0.938

## Usage

You can use cURL to access this model:

```
$ curl -X POST -H "Authorization: Bearer YOUR_API_KEY" -H "Content-Type: application/json" -d '{"inputs": "I love AutoTrain"}' https://api-inference.huggingface.co/models/frankielizcano/autotrain-train_player_org-1810562486
```

Or Python API:

```
from transformers import AutoModelForTokenClassification, AutoTokenizer

model = AutoModelForTokenClassification.from_pretrained("frankielizcano/autotrain-train_player_org-1810562486", use_auth_token=True)

tokenizer = AutoTokenizer.from_pretrained("frankielizcano/autotrain-train_player_org-1810562486", use_auth_token=True)

inputs = tokenizer("I love AutoTrain", return_tensors="pt")

outputs = model(**inputs)
```