# 🪐 Exoplanet Explorer Dashboard

An interactive dashboard built with **Streamlit** that visualizes real exoplanet data from NASA's Exoplanet Archive, with AI-powered summaries via **Google Gemini**.

> No heavy local models. Fully deployable on Streamlit Cloud free tier.

---

## ✨ Features

- 🔭 **Live NASA Data** — Pulls directly from the NASA Exoplanet Archive TAP API (5,000+ confirmed planets)
- 📅 **Timeline of Discoveries** — Stacked bar chart showing discoveries per year by method
- 🔵 **Size vs Distance Scatter** — Interactive plot with habitable zone overlay
- 🌱 **Habitable Zone Analysis** — Map of planets meeting Earth-like conditions with top candidates list
- 🤖 **Gemini AI Summaries** — One-click AI-generated insights about your filtered dataset
- 🔧 **Sidebar Filters** — Filter by discovery method, year range, planet radius, habitable zone

---

## 📁 Project Structure

```
├── app.py              # Main Streamlit app
├── nasa_api.py         # NASA Exoplanet Archive TAP API client
├── ai_summary.py       # Google Gemini AI summary module
├── requirements.txt    # Python dependencies
├── .env                # API keys (local only, never commit)
└── .streamlit/
    └── secrets.toml    # API keys for Streamlit Cloud deployment
```

---

## ⚙️ Local Setup

### 1. Clone & install

```bash
git clone https://github.com/your-username/exoplanet-dashboard.git
cd exoplanet-dashboard
pip install -r requirements.txt
```

### 2. Add your Gemini API key

Create a `.env` file:

```env
GEMINI_API_KEY=your_gemini_api_key_here
```

Get a free key at: [aistudio.google.com](https://aistudio.google.com)

### 3. Run

```bash
streamlit run app.py
```

---

## 🚀 Deploy to Streamlit Cloud

1. Push your project to a **public GitHub repository**
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set your secret in the Streamlit Cloud dashboard:
   - Go to **App Settings → Secrets**
   - Add:
     ```toml
     GEMINI_API_KEY = "your_gemini_api_key_here"
     ```
4. Click **Deploy** — that's it!

> ⚠️ Never commit your `.env` file. Add it to `.gitignore`.

---

## 🌱 Habitable Zone Criteria

The dashboard uses these simplified criteria to flag potentially habitable planets:

| Parameter | Range |
|---|---|
| Orbital distance | 0.5 – 2.0 AU |
| Host star temperature | 3,700 – 7,200 K |

These approximate the conditions where liquid water could exist on a planet's surface.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| Streamlit | Web UI & deployment |
| Plotly | Interactive charts |
| Pandas | Data processing |
| NASA Exoplanet Archive | Planet data (free, no API key needed) |
| Google Gemini API | AI summaries (free tier) |

---

## 📄 License

MIT — free to use and modify.
