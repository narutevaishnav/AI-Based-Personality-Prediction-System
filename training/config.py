import torch

# Dataset Path
DATA_PATH = "dataset/OCEAN-synthetic.csv"

# Pretrained BERT Model
MODEL_NAME = "bert-base-uncased"

# Saved Model Folder
MODEL_SAVE_PATH = "saved_model/"

# Training Parameters
MAX_LENGTH = 128
BATCH_SIZE = 8
EPOCHS = 3
LEARNING_RATE = 1e-5

# Device
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")