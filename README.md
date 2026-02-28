# 🪐 Exoplanet Explorer Dashboard

An interactive data dashboard that pulls live data from NASA's Exoplanet Archive and lets you explore 5,000+ confirmed exoplanets through dynamic charts  discovery timelines, planet size vs orbital distance, and a habitable zone map highlighting Earth-like candidates. Powered by Groq's Llama 3.3 70B for instant AI-generated insights on any filtered dataset. Built with Streamlit and deployable to Streamlit Cloud in minutes with zero heavy dependencies or local models.

---

## ✨ Features

- 🔭 **Live NASA Data** — Pulls directly from the NASA Exoplanet Archive TAP API (5,000+ confirmed planets, no API key needed)
- 📅 **Timeline of Discoveries** — Stacked bar chart showing discoveries per year broken down by method
- 🔵 **Size vs Distance Scatter** — Interactive bubble chart with habitable zone overlay
- 🌱 **Habitable Zone Analysis** — Map of planets meeting Earth-like conditions with top candidates list
- 🤖 **AI Summaries** — One-click insights powered by Groq (Llama 3.3 70B) on your filtered dataset
- 🔧 **Sidebar Filters** — Filter by discovery method, year range, planet radius, and habitable zone

---

## 📁 Project Structure

```
├── app.py              # Main Streamlit app
├── nasa_api.py         # NASA Exoplanet Archive TAP API client
├── ai_summary.py       # Groq AI summary module
├── requirements.txt    # Python dependencies
├── .env                # API keys (local only, never commit)
├── .gitignore
└── .streamlit/
    └── secrets.toml    # API keys for Streamlit Cloud
```

---

## ⚙️ Local Setup

### 1. Clone & install

```bash
git clone https://github.com/Krishankant89/exoplanet-dashboard.git
cd exoplanet-dashboard
pip install -r requirements.txt
```

### 2. Add your Groq API key

Create a `.env` file in the root directory:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Get a free key at: [console.groq.com](https://console.groq.com)

### 3. Run

```bash
streamlit run app.py
```

---

## 🚀 Deploy to Streamlit Cloud

1. Push your project to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. In **App Settings → Secrets**, add:
   ```toml
   GROQ_API_KEY = "your_groq_api_key_here"
   ```
4. Click **Deploy** — done!

> ⚠️ Never commit your `.env` or `.streamlit/secrets.toml` — both are in `.gitignore`.

---

## 🌱 Habitable Zone Criteria

The dashboard uses these simplified criteria to flag potentially habitable planets:

| Parameter | Range |
|---|---|
| Orbital distance | 0.5 – 2.0 AU |
| Host star temperature | 3,700 – 7,200 K |

These approximate the conditions where liquid water could exist on a planet's surface, similar to Earth's position around the Sun.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Web UI & deployment |
| Plotly | Interactive charts |
| Pandas | Data processing |
| NASA Exoplanet Archive | Planet data (free, no key needed) |
| Groq — Llama 3.3 70B | AI summaries (free tier, 14,400 req/day) |

---

## 📄 License

MIT — free to use and modify.