import torch
import torch.nn as nn
from transformers import BertModel

from training.config import MODEL_NAME


class OceanBERT(nn.Module):
    def __init__(self):
        super(OceanBERT, self).__init__()

        self.bert = BertModel.from_pretrained(MODEL_NAME)

        self.dropout = nn.Dropout(0.3)

        self.regressor = nn.Linear(768, 5)

    def forward(self, input_ids, attention_mask):
        outputs = self.bert(
            input_ids=input_ids,
            attention_mask=attention_mask
        )

        pooled_output = outputs.pooler_output

        pooled_output = self.dropout(pooled_output)

        prediction = self.regressor(pooled_output)

        return prediction