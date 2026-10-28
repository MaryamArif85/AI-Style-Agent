✨ StyleSync AI — Autonomous Multi-Agent Personal Stylist for Pakistani Fashion

StyleSync AI is an advanced, state-aware multi-agent fashion stylist built using **LangGraph**, **LangChain**, **Groq (OPENAI GPT-120B)**, and **OpenCV**. It is custom-tailored for the Pakistani retail and unstitched fabric market, helping users coordinate outfits, analyze skin-tone color palettes, and generate precision-filtered search links across top local brands.

---

## 🌟 Key Features

1. **Autonomous LangGraph Architecture**: Manages multi-step reasoning with shared state (`AgentState`), explicit processing nodes, and conditional routing.
2. **Computer Vision Skin Analysis**: Automatically extracts RGB color values and skin undertones from uploaded hand, arm, or face photos using OpenCV.
3. **Tool-Augmented Search (`@tool`)**: Dynamically binds LangChain tools to generate direct filtered product search URLs for top Pakistani brands (**Khaadi, Sapphire, Ethnic, Cross Stitch, Gul Ahmed, Junaid Jamshed (J.), Limelight, Bonanza Satrangi, Sana Safinaz, Alkaram Studio, Outfitters**).
4. **Accessory & Footwear Pairing**: Automatically computes matching footwear search links (Stylo and Borjan) calibrated to skin tones.
5. **Multi-Key Round-Robin Failover**: Built-in API key rotation prevents token exhaustion and rate-limit errors during live presentations.
6. **Custom Unstitched Fabric Tailoring**: Analyzes market fabric photos and generates bespoke tailoring blueprints (necklines, sleeve designs, trouser cuts).

---

<!-- ## 📸 User Interface Preview -->

## 🛠️ Project Structure

```text
StyleSync-AI/
├── .env.example               # Environment variable template
├── .gitignore                 # Git exclusion rules
├── requirements.txt           # Python dependencies
├── config.py                  # API key rotation manager & brand constants
├── agent_graph.py             # LangGraph State, Nodes, Edges & Tool Definitions
├── vision_utils.py            # OpenCV skin tone & color palette extractor
└── app.py                     # Streamlit luxury boutique user interface
```

---

## 🚀 Local Installation & Setup

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MaryamArif85/AI-Style-Agent
   cd ai-style-agent
   ```

2. **Create and Activate a Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**:
   Create a `.env` file in the root directory based on `.env.example`:
   ```env
   
   GROQ_KEY_1=PASTE KEY HERE
   GROQ_KEY_2=PASTE KEY HERE
   GROQ_KEY_3=PASTE KEY HERE
   GROQ_MODEL="openai-gpt4-oss-120b"
   LANGSMITH_TRACING="true"
   LANGSMITH_API_KEY=""
   LANGSMITH_PROJECT="stylesync-ai-agent"
   ```

5. **Run the Streamlit Application**:
   ```bash
   streamlit run app.py
   ```

---

