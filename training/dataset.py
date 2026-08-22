import pandas as pd
import torch
from torch.utils.data import Dataset
from transformers import BertTokenizer

from training.config import MODEL_NAME, MAX_LENGTH


class OceanDataset(Dataset):
    def __init__(self, csv_file):
        # Load dataset
        self.data = pd.read_csv(csv_file)

        # Remove rows with missing values
        self.data = self.data.dropna()

        # Keep only valid OCEAN scores (1 to 5)
        traits = [
            "Openness",
            "Conscientiousness",
            "Extraversion",
            "Agreeableness",
            "Neuroticism",
        ]

        for col in traits:
            self.data = self.data[
                (self.data[col] >= 1.0) &
                (self.data[col] <= 5.0)
            ]

        # Reset index after filtering
        self.data = self.data.reset_index(drop=True)

        print(f"Dataset after cleaning: {len(self.data)} samples")

        # Load tokenizer
        self.tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

        # Text column
        self.texts = self.data["Text"].astype(str)

        # OCEAN Labels
        self.labels = self.data[
            [
                "Openness",
                "Conscientiousness",
                "Extraversion",
                "Agreeableness",
                "Neuroticism",
            ]
        ].values.astype("float32")

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        text = self.texts.iloc[idx]
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            padding="max_length",
            truncation=True,
            max_length=MAX_LENGTH,
            return_tensors="pt",
        )

        return {
            "input_ids": encoding["input_ids"].squeeze(0),
            "attention_mask": encoding["attention_mask"].squeeze(0),
            "labels": torch.tensor(label, dtype=torch.float),
        }