"""
chatbot.py - Assistant principal (AI Niveau 1).

Given a user question, searches data/hel_content.json for the most
relevant page and returns an excerpt + the source URL + confidence.
"""

import json
import re
#json (to read the file) and re (to extract words)

# Path to the scraped HEL data
DATA_FILE = "data/hel_content.json"


# Small French stopwords list (words we ignore when matching)
STOPWORDS = {
     "le", "la", "les", "un", "une", "des", "de", "du", "et", "ou",
    "au", "aux", "ce", "cette", "ces", "se", "sa", "son", "ses",
    "mon", "ma", "mes", "ton", "ta", "tes", "leur", "leurs",
    # Verbs and helpers
    "est", "sont", "été", "avoir", "être", "fait", "faire", "fais",
    "ai", "as", "ont", "aura", "sera",
    # Question words
    "que", "qui", "quoi", "quel", "quelle", "quels", "quelles",
    "comment", "où", "quand", "pourquoi",
    # Prepositions / connectors
    "pour", "par", "avec", "sans", "sur", "sous", "dans", "en",
    "ne", "pas", "non", "oui", "si",
    # Pronouns
    "je", "tu", "il", "elle", "nous", "vous", "ils", "elles",
    "y", "me", "te", "lui",
    # HEL-specific (every page mentions HEL, useless for matching)
    "hel", "haute", "ecole", "école", "ville", "liège", "liege",
    # Time/weather words
    "temps", "aujourd", "hui", "an", "ans", "année", "années", 
}


# ===== Hardcoded Q&A (A1) =====
HARDCODED_QA = [
    {
        "keywords": ["téléphone", "telephone", "contact", "numéro","numero", "appeler"],
        "answer": "Le numéro de contact général de la HEL est le 04/238.38.00. Sciences et Techniques : 04/254.10.10 — Sciences de l'Education : 04/258.40.50 — Paramédical : 04/258.42.22 — Sciences Economiques : 04/258.42.30.",
        "source": "https://www.hel.be/",
        "confidence": "elevee"
    },

    {
        "keywords": ["portes ouvertes", "porte ouverte", "journée", "visite", "evenement", "événement"],
        "answer": "Les journées portes ouvertes de la HEL ont lieu le 27 juin 2026 de 09h00 à 12h00 et le 2 septembre 2026 de 13h00 à 17h00.",
        "source": "https://www.hel.be/",
        "confidence": "elevee"
    },
    {
        "keywords": ["adresse", "trouve", "situe", "situé", "localisation", "lieu", "campus"],
        "answer": "La HEL est située en plein centre de Liège. Le siège principal est au Boulevard d'Avroy n°5 – 4000 Liège. Elle dispose de plusieurs implantations : Jonfosse, Sohet, Quai du Condroz et Rue de Londres.",
        "source": "https://www.hel.be/implantations/",
        "confidence": "elevee"
    },
    {
        "keywords": ["inscription", "inscrire", "date", "délai", "quand"],
        "answer": "Les inscriptions pour les étudiants belges et européens sont ouvertes du 15/04/2026 au 30/09/2026. Pour les étudiants hors UE non assimilés : les 9 et 10/03/2026.",
        "source": "https://www.hel.be/inscriptions/",
        "confidence": "elvee"
    },
    {
        "keywords": ["formation", "bachelier", "cursus", "études", "etudes", "programme"],
        "answer": "La HEL propose plusieurs bacheliers : Informatique, Comptabilité, Automobile, Chimie, Electronique, Logopédie, Relations publiques, Gestion hôtelière, Energies alternatives, et des Masters en enseignement.",
        "source": "https://www.hel.be/",
        "confidence": "elevee"
    },

    # ===== Category: Frais =====
    {
        "keywords": ["frais", "coût", "cout", "payer", "prix", "tarif", "droit", "droits"],
        "answer": "Les frais d'inscription à la HEL varient selon votre situation. Pour les étudiants réguliers, le droit d'inscription est fixé par la Communauté française. Des réductions sont possibles via le service social. Contactez le secrétariat au 04/238.38.00 pour plus d'informations.",
        "source": "https://www.hel.be/ue-frais-inscription/",
        "confidence": "elevee"
    },
    {
        "keywords": ["bourse", "aide financière", "reduction", "réduction", "cpas", "social"],
        "answer": "La HEL propose des aides financières via son Service Social : réduction des droits d'inscription, aides du CPAS, bourses d'études. Contactez le service social pour connaître vos droits.",
        "source": "https://www.hel.be/ue-frais-inscription/",
        "confidence": "elevee"
    },
    # ===== Category: Enseignants =====
    {
        "keywords": ["enseignant", "professeur", "prof", "teacher", "formateur", "encadrement"],
        "answer": "Les enseignants de la HEL sont des professionnels expérimentés et disponibles. La HEL privilégie les petites classes pour un encadrement personnalisé. 100% des employeurs estiment que les diplômés maîtrisent bien leurs compétences professionnelles.",
        "source": "https://www.hel.be/",
        "confidence": "elevee"
    },
    {
        "keywords": ["contact", "secrétariat", "secretariat", "bureau", "rendez-vous"],
        "answer": "Vous pouvez contacter les enseignants via les secrétariats de chaque département : Sciences et Techniques : 04/254.10.10 — Sciences de l'Education : 04/258.40.50 — Paramédical : 04/258.42.22 — Sciences Economiques : 04/258.42.30.",
        "source": "https://www.hel.be/",
        "confidence": "elevee"
    },
]


def check_hardcoded(question):
    """Check if the question matches any hardcoded Q&A."""
    question_lower = question.lower()
    for qa in HARDCODED_QA:
        for keyword in qa["keywords"]:
            if keyword in question_lower:
                return {
                    "answer": qa["answer"],
                    "source": qa["source"],
                    "confidence": qa["confidence"],
                }
    return None


def load_pages():
    """Read the scraped HEL pages from the JSON file."""
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
    
#it reads whater is wrriten on DATA_FILE and ,save it on f and then close the file using with ()as var:


def extract_keywords(question):
    """Pull the useful words from a question (lowercase, no stopwords)."""
    words = re.findall(r"\w+", question.lower()) #re.findall(pattren,text)
    return [w for w in words if w not in STOPWORDS and len(w) > 2]
#it stors the words from the quetion on a list depending on a pattern 

def score_page(content, keywords):
    """Count how many times the keywords appear in one page."""
    content_lower = content.lower()
    return sum(content_lower.count(kw) for kw in keywords)
#it count how many a word apperes on a page and sum it (We will use it to verify the page's validity.)

def best_excerpt(content, keywords, window=600):
    """Find the chunk of text inside a page where most keywords appear."""
    content_lower = content.lower()
    best_score = 0
    best_pos = 0

    step = 200
    end = max(1, len(content) - window)
    for i in range(0, end, step):
        section = content_lower[i:i + window]
        score = sum(section.count(kw) for kw in keywords)
        if score > best_score:
            best_score = score
            best_pos = i

    excerpt = content[best_pos:best_pos + window]
    if best_pos > 0:
        excerpt = "..." + excerpt
    if best_pos + window < len(content):
        excerpt = excerpt + "..."
    return excerpt


def find_answer(question):
    """
    Main function. Returns a dict:
        - answer:     the relevant text excerpt
        - source:     the HEL URL where it came from
        - confidence: 'elevee', 'moyenne', or 'faible'
    """
    # Check hardcoded Q&A first
    hardcoded = check_hardcoded(question)
    if hardcoded:
        return hardcoded


    keywords = extract_keywords(question)

    if not keywords:
        return {
            "answer": "Veuillez poser une question plus précise.",
            "source": None,
            "confidence": "faible",
        }

    pages = load_pages()
    best_page = None
    best_score = 0

    for page in pages:
        score = score_page(page["content"], keywords)
        if score > best_score:
            best_score = score
            best_page = page

    # No decent match found
    if best_score < 2 or best_page is None:
        return {
            "answer": "Je n'ai pas trouvé de réponse fiable dans les données de la HEL. Essayez de reformuler votre question.",
            "source": None,
            "confidence": "faible",
        }

    # Decide the confidence label based on the score
    if best_score >= 6:
        confidence = "elevee"
    elif best_score >= 3:
        confidence = "moyenne"
    else:
        confidence = "faible"

    return {
        "answer": best_excerpt(best_page["content"], keywords),
        "source": best_page["url"],
        "confidence": confidence,
    }


# Quick self-test — run "python chatbot.py" to test in terminal
if __name__ == "__main__":
    test_questions = [
        "Comment s'inscrire à la HEL ?",
        "Bachelier en informatique",
        "Bachelier en comptabilité",
        "Quel temps fait-il aujourd'hui ?",
    ]
    for q in test_questions:
        print("\n" + "=" * 60)
        print(f"Question: {q}")
        result = find_answer(q)
        print(f"Confiance: {result['confidence']}")
        print(f"Source:    {result['source']}")
        print(f"Réponse:   {result['answer'][:250]}...")