import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# Read individual GROQ_KEY_* variables
GROQ_KEYS = []
for key_name in ["GROQ_KEY_1", "GROQ_KEY_2", "GROQ_KEY_3", "GROQ_API_KEY"]:
    val = os.getenv(key_name, "").strip().strip('"').strip("'")
    if val and not val.startswith("your_") and not val.startswith("gsk_key"):
        GROQ_KEYS.append(val)

# Fallback: if keys are passed in GROQ_API_KEYS (comma separated)
if not GROQ_KEYS:
    raw_keys = os.getenv("GROQ_API_KEYS", "")
    GROQ_KEYS = [k.strip().strip('"').strip("'") for k in raw_keys.split(",") if k.strip() and "your_" not in k]

if not GROQ_KEYS:
    raise ValueError(
        "❌ No valid Groq API key found! Please check your .env file and set GROQ_KEY_1='gsk_...'"
    )

GROQ_MODEL = os.getenv("GROQ_MODEL", "gpt-4o-mini").strip().strip('"').strip("'")

_current_key_index = 0

def get_next_groq_client(temperature=0.7):
    """Rotates through available Groq API keys to prevent token/rate-limit errors."""
    global _current_key_index
    key = GROQ_KEYS[_current_key_index]
    
    # Terminal debug print to verify key loading
    masked = key[:6] + "..." + key[-4:] if len(key) > 10 else "INVALID"
    print(f"🔑 Using Groq Key #{_current_key_index + 1} ({masked}) with model '{GROQ_MODEL}'")
    
    _current_key_index = (_current_key_index + 1) % len(GROQ_KEYS)
    
    return ChatGroq(
        temperature=temperature,
        model_name=GROQ_MODEL,
        groq_api_key=key
    )

PAK_BRANDS = [
    "Khaadi",
    "Sapphire",
    "Gul Ahmed",
    "Junaid Jamshed (J.)",
    "Ethnic",
    "Cross Stitch",
    "Limelight",
    "Bonanza Satrangi",
    "Sana Safinaz",
    "Alkaram Studio",
    "Outfitters"
]