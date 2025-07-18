#!/usr/bin/env python3
import os
from transformers import AutoTokenizer, AutoModelForMaskedLM

tokenizer = AutoTokenizer.from_pretrained("google-bert/bert-base-cased")
model = AutoModelForMaskedLM.from_pretrained("google-bert/bert-base-cased")

models_dir = os.path.join("resource", "bert-base-cased")
tokenizer.save_pretrained(models_dir)
model.save_pretrained(models_dir)
