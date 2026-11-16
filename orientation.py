"""
orientation.py - Orientation IA
Takes student interests and recommends the best HEL formation.
"""

import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Load HEL formations from the data file
with open("data/hel_content.json", "r", encoding="utf-8") as f:
    hel_data = json.load(f)

# Extract just the formations list as text
formations_text = "\n".join([
    f"- {item['url']}: {item['content'][:300]}"
    for item in hel_data
])


def get_orientation(interests):
    """
    Takes student interests and returns a formation recommendation.
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"""Tu es un conseiller d'orientation pour la Haute École de la Ville de Liège (HEL).
Voici les formations disponibles à la HEL:
{formations_text}

Quand un étudiant décrit ses intérêts, tu dois:
1. Recommander la formation la plus adaptée
2. Expliquer pourquoi en 2-3 phrases
3. Mentionner les débouchés professionnels
Réponds toujours en français de manière encourageante et claire."""
            },
            {
                "role": "user",
                "content": f"Mes intérêts et passions sont: {interests}"
            }
        ]
    )
    return response.choices[0].message.content