"""
orchestrator.py - Niveau 3 : IA Orchestrateur
Reads the question and decides which AI to use.
"""

import os
from groq import Groq
from dotenv import load_dotenv
from chatbot import find_answer
from chatbot_advanced import ask_claude

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def classify_question(question):
    """
    Ask Groq to classify the question.
    Returns either "HEL" or "GENERAL"
    """
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "Tu es un classificateur. On te donne une question. Réponds UNIQUEMENT par le mot HEL si la question concerne la Haute École de la Ville de Liège (formations, inscriptions, implantations, débouchés, services). Réponds UNIQUEMENT par le mot GENERAL si la question est générale. Un seul mot, rien d'autre."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )
    result = response.choices[0].message.content.strip().upper()
    return result


# def orchestrate(question):
#     """
#     Main function: classify then route to the right AI.
#     """
#     category = classify_question(question)

#     if category == "HEL":
#         result = find_answer(question)
#         result["niveau"] = "Niveau 1 — Assistant principal"
#         return result
#     else:
#         answer = ask_claude(question)
#         return {
#             "answer": answer,
#             "source": None,
#             "confidence": "élevée",
#             "niveau": "Niveau 2 — Assistant IA"
#         }

def orchestrate(question):
    """
    Main function: classify then route to the right AI.
    """
    category = classify_question(question)

    if category == "HEL":
        return {
            "answer": "Pour cette question, je vous recommande d'utiliser l'Assistant principal qui est spécialisé dans les données officielles de la HEL.",
            "source": None,
            "confidence": "élevée",
            "niveau": "Niveau 1 — Assistant principal",
            "redirect": "/chat"
        }
    else:
        answer = ask_claude(question)
        return {
            "answer": answer,
            "source": None,
            "confidence": "élevée",
            "niveau": "Niveau 2 — Assistant IA",
            "redirect": None
        }