import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from training.config import (
    DATA_PATH,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    DEVICE,
    MODEL_SAVE_PATH,
)

from training.dataset import OceanDataset
from training.model import OceanBERT


def train():
    print("Loading dataset...")
    dataset = OceanDataset(DATA_PATH)

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    print(f"Dataset Loaded Successfully! Total Samples: {len(dataset)}")

    print("Loading BERT model...")
    model = OceanBERT().to(DEVICE)
    print(f"Using Device: {DEVICE}")

    criterion = nn.MSELoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE
    )

    model.train()

    print("\n========== Training Started ==========\n")

    for epoch in range(EPOCHS):

        print(f"\n========== Epoch {epoch + 1}/{EPOCHS} ==========\n")

        total_loss = 0

        import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from training.config import (
    DATA_PATH,
    BATCH_SIZE,
    EPOCHS,
    LEARNING_RATE,
    DEVICE,
    MODEL_SAVE_PATH,
)

from training.dataset import OceanDataset
from training.model import OceanBERT


def train():
    print("Loading dataset...")
    dataset = OceanDataset(DATA_PATH)

    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True
    )

    print(f"Dataset Loaded Successfully! Total Samples: {len(dataset)}")

    print("Loading BERT model...")
    model = OceanBERT().to(DEVICE)
    print(f"Using Device: {DEVICE}")

    criterion = nn.MSELoss()

    optimizer = torch.optim.AdamW(
        model.parameters(),
        lr=LEARNING_RATE
    )

    model.train()

    print("\n========== Training Started ==========\n")

    for epoch in range(EPOCHS):

        print(f"\n========== Epoch {epoch + 1}/{EPOCHS} ==========\n")

        total_loss = 0.0

        for batch_idx, batch in enumerate(dataloader):

            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["labels"].to(DEVICE)

            optimizer.zero_grad()

            outputs = model(input_ids, attention_mask)

            # Print first batch only
            if batch_idx == 0 and epoch == 0:
                print("\n========== Debug ==========")
                print("Sample Predictions:")
                print(outputs[:3].detach().cpu())

                print("\nSample Labels:")
                print(labels[:3].cpu())
                print("===========================\n")

            loss = criterion(outputs, labels)

            # Stop if loss becomes NaN
            if torch.isnan(loss):
                print(f"\n❌ NaN loss detected at Batch {batch_idx + 1}")
                return

            loss.backward()

            # Gradient clipping
            torch.nn.utils.clip_grad_norm_(
                model.parameters(),
                max_norm=1.0
            )

            optimizer.step()

            total_loss += loss.item()

            if (batch_idx + 1) % 10 == 0:
                print(
                    f"Batch {batch_idx + 1}/{len(dataloader)} | "
                    f"Loss: {loss.item():.4f}"
                )

        avg_loss = total_loss / len(dataloader)

        print(f"\nEpoch {epoch + 1} Completed")
        print(f"Average Loss: {avg_loss:.4f}")

    print("\nSaving model...")

    torch.save(
        model.state_dict(),
        MODEL_SAVE_PATH + "ocean_bert.pth"
    )

    print("\n==============================")
    print("Training Completed Successfully!")
    print(f"Model saved at: {MODEL_SAVE_PATH}ocean_bert.pth")
    print("==============================")


if __name__ == "__main__":
    train()