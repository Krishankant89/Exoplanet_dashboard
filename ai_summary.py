import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_ai_summary(stats: dict) -> str:
    """
    Generate an AI summary of the current exoplanet dataset using Groq.

    Args:
        stats: dict with keys like total_planets, year_range, top_methods,
               avg_radius, avg_distance, habitable_zone_count, etc.
    Returns:
        A formatted string summary.
    """
    try:
        prompt = f"""You are an expert astronomer and science communicator. Analyze the following exoplanet dataset statistics and write a clear, engaging, and insightful 3-4 paragraph summary.

Dataset Statistics:
- Total planets shown: {stats.get('total_planets', 'N/A')}
- Discovery year range: {stats.get('year_range', 'N/A')}
- Top discovery methods: {stats.get('top_methods', {})}
- Average planet radius: {stats.get('avg_radius', 'N/A')} Earth radii
- Average orbital distance: {stats.get('avg_distance', 'N/A')} AU
- Planets in habitable zone: {stats.get('habitable_zone_count', 'N/A')}
- Discovery method filter applied: {stats.get('filter_method', 'All')}
- Habitable zone filter active: {stats.get('habitable_only', False)}

Your summary should:
1. Highlight key trends and interesting findings from this data
2. Explain what the habitable zone results mean for the search for life
3. Comment on the dominant discovery methods and what they tell us
4. End with an exciting forward-looking statement about exoplanet science

Keep the tone engaging and accessible to a general audience.
Write in flowing paragraphs, not bullet points.
"""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert astronomer and engaging science communicator."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=600
        )

        return response.choices[0].message.content

    except Exception as e:
        return f"Could not generate AI summary: {str(e)}\nPlease check your GROQ_API_KEY in the .env file."