# Importing stock libraries
import numpy as np
import pandas as pd
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader
from torch import cuda
# Importing the T5 modules from huggingface/transformers
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Creating a custom dataset for reading the dataframe and loading it into the dataloader to pass it to the neural network at a later stage for finetuning the model and to prepare it for predictions

class CustomDataset(Dataset):

    def __init__(self, dataframe, tokenizer, source_len, summ_len):
        self.tokenizer = tokenizer
        self.data = dataframe
        self.source_len = source_len
        self.summ_len = summ_len
        self.text = self.data.text
        self.ctext = self.data.ctext

    def __len__(self):
        return len(self.text)

    def __getitem__(self, index):
        ctext = str(self.ctext[index])
        ctext = ' '.join(ctext.split())

        text = str(self.text[index])
        text = ' '.join(text.split())

        source = self.tokenizer.batch_encode_plus([ctext], max_length= self.source_len, pad_to_max_length=True,return_tensors='pt')
        target = self.tokenizer.batch_encode_plus([text], max_length= self.summ_len, pad_to_max_length=True,return_tensors='pt')

        source_ids = source['input_ids'].squeeze()
        source_mask = source['attention_mask'].squeeze()
        target_ids = target['input_ids'].squeeze()
        target_mask = target['attention_mask'].squeeze()

        return {
            'source_ids': source_ids.to(dtype=torch.long), 
            'source_mask': source_mask.to(dtype=torch.long), 
            'target_ids': target_ids.to(dtype=torch.long),
            'target_ids_y': target_ids.to(dtype=torch.long)
        }

def generate(tokenizer, model, device, text):
    MAX_LEN = 512
    SUMMARY_LEN = 50 
    VALID_BATCH_SIZE = 5

    val_dataset= pd.DataFrame([["",text]],columns=["text","ctext"])

    val_set = CustomDataset(val_dataset, tokenizer, MAX_LEN, SUMMARY_LEN)

    val_params = {
            'batch_size': VALID_BATCH_SIZE,
            'shuffle': False,
            'num_workers': 0
            }

    loader = DataLoader(val_set, **val_params)
    predictions = []
    with torch.no_grad():
        for _, data in enumerate(loader, 0):
            ids = data['source_ids'].to(device, dtype = torch.long)
            mask = data['source_mask'].to(device, dtype = torch.long)

            generated_ids = model.generate(
                input_ids = ids,
                attention_mask = mask, 
                max_length=150, 
                num_beams=2,
                repetition_penalty=2.5, 
                length_penalty=1.0, 
                early_stopping=True
                )
            preds = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=True) for g in generated_ids]

            predictions.extend(preds)

    response = predictions[0]
    if response[0].isupper():
        clean_response = ".".join(response.split(".")[:-1])
    else:
        clean_response = ".".join(response.split(".")[1:-1])

    return clean_response

def load_model_summarization():
    # Setting up the device for GPU usage
    device = 'cuda' if cuda.is_available() else 'cpu'

    tokenizer = T5Tokenizer.from_pretrained("t5-base")

    model = T5ForConditionalGeneration.from_pretrained("./models/T5_summarization_model")
    model = model.to(device)

    print("Model and tokenizer for T5 loaded.")
    return device,tokenizer,model

# device,tokenizer,model = load_model_summarization()

# text = """I walked the floor of storage. I have walked the floor of cafeteria. I entered storage. I entered electrical. I entered storage. I saw Black. I saw more Black. I entered electrical. I have finished the Calibrate Distributor task. I entered storage. I entered shields. I entered oxygen. I entered weapons. I entered cafeteria. I entered admin. I saw Blue. I saw more Blue. I finished the Swipe Card task. I walked the floor of storage. I walked the floor of electrical. I have finished the Calibrate Distributor task. I entered storage. I have walked on shields soil. I entered oxygen. I have walked on shields soil. I walked the floor of storage. I walked the floor of electrical. I have finished the Calibrate Distributor task. I walked the floor of storage. I entered shields. I entered oxygen. I entered shields. I walked the floor of storage. I walked the floor of electrical. I have finished the Calibrate Distributor task. I finished the Divert Power task. I entered lower engine. I have stepped on the floor of security. I saw Green. I saw more Green. I finished the Accept Power (security) task."""

# test = generate(tokenizer, model, device, text)[0]
# print(test)