import os
import torch
from transformers import BertTokenizer
from huggingface_hub import hf_hub_download

from training.model import OceanBERT
from training.config import (
    MODEL_NAME,
    MODEL_SAVE_PATH,
    MAX_LENGTH,
    DEVICE,
)

# -----------------------------
# Hugging Face Hub Settings
# -----------------------------
# TODO: ithe tuza Hugging Face model repo cha naav taak
# example: "narutevaishnav/ocean-bert"
HF_REPO_ID = "narutevaishnav/ocean-bert-personality"
MODEL_FILENAME = "ocean_bert_hf.pth"

# -----------------------------
# Download model if not present locally
# -----------------------------
os.makedirs(MODEL_SAVE_PATH, exist_ok=True)

local_model_path = os.path.join(MODEL_SAVE_PATH, MODEL_FILENAME)

if not os.path.exists(local_model_path):

    print("Model not found locally. Downloading from Hugging Face Hub...")

    downloaded_path = hf_hub_download(
        repo_id=HF_REPO_ID,
        filename=MODEL_FILENAME,
        local_dir=MODEL_SAVE_PATH,
    )

    print("Model downloaded to:", downloaded_path)

# -----------------------------
# Load Tokenizer
# -----------------------------
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)

# -----------------------------
# Load Trained Model
# -----------------------------
model = OceanBERT()

model.load_state_dict(
    torch.load(
        local_model_path,
        map_location=DEVICE,
    )
)

model.to(DEVICE)
model.eval()

# -----------------------------
# Quantize model to reduce RAM usage
# (int8 quantization on Linear layers — cuts memory ~2-4x,
#  accuracy impact is minimal for this use case)
# -----------------------------
model = torch.quantization.quantize_dynamic(
    model,
    {torch.nn.Linear},
    dtype=torch.qint8,
)


# -----------------------------
# Convert Score to Level
# -----------------------------
def get_level(score):

    if score >= 4.0:
        return "Very High"

    elif score >= 3.0:
        return "High"

    elif score >= 2.0:
        return "Moderate"

    elif score >= 1.0:
        return "Low"

    else:
        return "Very Low"


# -----------------------------------
# Personality Descriptions
# -----------------------------------
descriptions = {

    # ==========================
    # OPENNESS
    # ==========================
    "Openness": {

        "Very High":
        "You are highly creative, curious, and open to exploring new ideas and experiences. You enjoy learning new skills, thinking outside the box, and adapting quickly to change. People often see you as imaginative, innovative, and willing to consider different perspectives. You enjoy challenges that require creativity and problem-solving.",

        "High":
        "You are curious and enjoy discovering new ideas and opportunities. You like learning new concepts and are comfortable trying different approaches to solve problems. Although you appreciate structure, you also welcome personal growth and continuous improvement.",

        "Moderate":
        "You have a balanced approach toward new experiences. You enjoy creativity when it is useful while also valuing practical and realistic solutions. This balance allows you to adapt without losing focus on your goals.",

        "Low":
        "You prefer familiar routines and practical solutions. You value stability, consistency, and proven methods over experimentation. You usually rely on experience when making decisions and prefer environments with predictable outcomes.",

        "Very Low":
        "You strongly value tradition, structure, and predictability. You prefer established methods instead of experimenting with new ideas. Your consistency and reliability make you dependable in structured environments."
    },

    # ==========================
    # CONSCIENTIOUSNESS
    # ==========================
    "Conscientiousness": {

        "Very High":
        "You are extremely organized, disciplined, dependable, and goal-oriented. You carefully plan your work, manage your time effectively, and consistently complete tasks before deadlines. People trust you because of your strong sense of responsibility and commitment.",

        "High":
        "You are responsible, reliable, and well organized. You enjoy planning your work and completing tasks efficiently. You are dependable and usually achieve your goals through dedication and consistent effort.",

        "Moderate":
        "You balance planning with flexibility. You complete important responsibilities while remaining adaptable when unexpected situations arise. You are dependable without becoming overly rigid.",

        "Low":
        "You prefer flexibility instead of strict schedules. You enjoy working in relaxed environments and may choose spontaneous approaches instead of detailed planning. You can still perform well when motivated.",

        "Very Low":
        "You enjoy freedom and spontaneity more than structured planning. Long-term organization may be challenging, but your flexibility allows you to adapt quickly to changing situations."
    },

    # ==========================
    # EXTRAVERSION
    # ==========================
    "Extraversion": {

        "Very High":
        "You are energetic, outgoing, and highly confident in social situations. You enjoy meeting new people, participating in group activities, and communicating your ideas openly. Others often see you as enthusiastic, approachable, and inspiring.",

        "High":
        "You enjoy social interaction and feel comfortable communicating with others. Teamwork, networking, and collaborative activities usually motivate you. You easily build relationships with people.",

        "Moderate":
        "You enjoy spending time with others but also appreciate quiet moments alone. You can comfortably work independently or within a team depending on the situation.",

        "Low":
        "You prefer calm environments and meaningful conversations with a small group of people. You may take time to open up but often build strong and lasting relationships.",

        "Very Low":
        "You are highly reserved and enjoy solitude. Independent work helps you focus, and you usually recharge by spending time alone instead of in large social gatherings."
    },    # ==========================
    # AGREEABLENESS
    # ==========================
    "Agreeableness": {

        "Very High":
        "You are compassionate, cooperative, and empathetic. You value harmony in relationships and genuinely care about the well-being of others. People often trust you because of your kindness, honesty, and willingness to help. You enjoy working in teams and maintaining positive relationships.",

        "High":
        "You are kind, supportive, and respectful toward others. You enjoy cooperating with people and usually resolve conflicts peacefully. Your friendly nature makes it easy for others to approach you.",

        "Moderate":
        "You maintain a healthy balance between kindness and assertiveness. You are willing to help others while also standing up for your own opinions when necessary.",

        "Low":
        "You are practical and direct when making decisions. You prefer logic over emotions and may appear more competitive than cooperative in certain situations.",

        "Very Low":
        "You are highly independent and strongly focused on achieving your own goals. You value honesty and direct communication more than emotional expression."
    },

    # ==========================
    # NEUROTICISM
    # ==========================
    "Neuroticism": {

        "Very High":
        "You may experience stress, anxiety, or emotional ups and downs more frequently than others. Challenging situations can affect your mood, but developing healthy coping strategies and emotional awareness can improve resilience and overall well-being.",

        "High":
        "You are emotionally sensitive and may worry during stressful situations. Although you sometimes experience self-doubt or anxiety, you are capable of managing these feelings with experience and support.",

        "Moderate":
        "You generally maintain emotional balance while occasionally experiencing stress in demanding situations. You recover from setbacks reasonably well and continue moving toward your goals.",

        "Low":
        "You usually remain calm and composed under pressure. You recover quickly from setbacks and rarely allow temporary problems to affect your long-term performance.",

        "Very Low":
        "You are emotionally stable, confident, and resilient. You handle stressful situations calmly and maintain a positive outlook even during difficult circumstances."
    }

}# -----------------------------------
# Prediction Function
# -----------------------------------

def generate_summary(prediction):

    summary = []

    if prediction["Openness"]["level"] in ["High", "Very High"]:
        summary.append(
            "You are creative, curious, and enjoy exploring new ideas."
        )
    else:
        summary.append(
            "You prefer practical solutions and familiar routines."
        )

    if prediction["Conscientiousness"]["level"] in ["High", "Very High"]:
        summary.append(
            "You are organized, responsible, and disciplined."
        )
    else:
        summary.append(
            "You prefer flexibility over strict planning."
        )

    if prediction["Extraversion"]["level"] in ["High", "Very High"]:
        summary.append(
            "You enjoy interacting with people and feel comfortable in social situations."
        )
    else:
        summary.append(
            "You are more comfortable in calm environments and enjoy personal space."
        )

    if prediction["Agreeableness"]["level"] in ["High", "Very High"]:
        summary.append(
            "You are kind, cooperative, and empathetic toward others."
        )
    else:
        summary.append(
            "You tend to make decisions based on logic and independence."
        )

    if prediction["Neuroticism"]["level"] in ["High", "Very High"]:
        summary.append(
            "You may experience stress more frequently and should focus on emotional well-being."
        )
    else:
        summary.append(
            "You remain emotionally stable and handle pressure well."
        )

    return " ".join(summary)


def predict_personality(text):

    encoding = tokenizer(
        text,
        padding="max_length",
        truncation=True,
        max_length=MAX_LENGTH,
        return_tensors="pt",
    )

    input_ids = encoding["input_ids"].to(DEVICE)
    attention_mask = encoding["attention_mask"].to(DEVICE)

    with torch.no_grad():
        output = model(input_ids, attention_mask)

    scores = output.squeeze().cpu().numpy()

    traits = [
        "Openness",
        "Conscientiousness",
        "Extraversion",
        "Agreeableness",
        "Neuroticism",
    ]

    prediction = {}

    for i, trait in enumerate(traits):

        score = round(float(scores[i]), 2)

        score = max(0.0, min(score, 5.0))

        level = get_level(score)

        prediction[trait] = {

            "score": score,

            "level": level,

            "description": descriptions[trait][level]

        }

    prediction["summary"] = generate_summary(prediction)

    return prediction


# -----------------------------------
# Testing
# -----------------------------------

if __name__ == "__main__":

    sample = input("Enter Social Media Post:\n\n")

    result = predict_personality(sample)

    print("\n========== OCEAN Personality ==========\n")

    for trait, info in result.items():

        if trait == "summary":
            continue

        print(f"{trait}")
        print(f"Score       : {info['score']}/5")
        print(f"Level       : {info['level']}")
        print(f"Description : {info['description']}")
        print("-" * 70)

    print("\nOverall Personality Summary\n")
    print(result["summary"])