import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def ask_claude(question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": "Tu es un assistant intelligent de la Haute École de la Ville de Liège (HEL). Réponds toujours en français de manière claire et utile."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message.content