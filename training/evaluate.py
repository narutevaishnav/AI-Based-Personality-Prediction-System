import torch
import numpy as np
from torch.utils.data import DataLoader
from sklearn.metrics import mean_squared_error, mean_absolute_error

from training.config import (
    DATA_PATH,
    BATCH_SIZE,
    DEVICE,
    MODEL_SAVE_PATH,
)

from training.dataset import OceanDataset
from training.model import OceanBERT


def evaluate():

    # Load Dataset
    dataset = OceanDataset(DATA_PATH)
    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False
    )

    # Load Trained Model
    model = OceanBERT()
    model.load_state_dict(
        torch.load(
            MODEL_SAVE_PATH + "ocean_bert.pth",
            map_location=DEVICE
        )
    )

    model.to(DEVICE)
    model.eval()

    predictions = []
    actuals = []

    with torch.no_grad():

        for batch in dataloader:

            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].cpu().numpy()

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask
            )

            predictions.extend(outputs.cpu().numpy())
            actuals.extend(labels)

    predictions = np.array(predictions)
    actuals = np.array(actuals)

    mse = mean_squared_error(actuals, predictions)
    mae = mean_absolute_error(actuals, predictions)

    print("\n========== Evaluation Result ==========\n")

    print(f"Mean Squared Error (MSE) : {mse:.4f}")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")

    print("\n=======================================\n")


if __name__ == "__main__":
    evaluate()