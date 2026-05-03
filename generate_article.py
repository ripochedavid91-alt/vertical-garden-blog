#!/usr/bin/env python3
import os, sys, datetime, re, requests, textwrap

# -------------------------------------------------
#  TOKEN HUGGING FACE (sera fourni via secret GitHub)
# -------------------------------------------------
HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL = "gpt2-medium"                     # modèle gratuit, suffisant pour nos besoins
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

def hf_generate(prompt: str, max_new_tokens: int = 500) -> str:
    """
    Appel à l'API d'inférence Hugging Face.
    Retourne le texte généré.
    """
    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": max_new_tokens,
            "temperature": 0.9
        }
    }
    r = requests.post(
        f"https://api-inference.huggingface.co/models/{MODEL}",
        headers=HEADERS,
        json=payload
    )
    r.raise_for_status()
    return r.json()[0]["generated_text"]

def slugify(text: str) -> str:
    """Transforme un titre en slug URL‑friendly."""
    return "-".join(re.sub(r"[^\w\s-]", "", text.lower()).split())[:80]

# -------------------------------------------------
#  1️⃣  Définir la niche (nous allons passer le texte en argument)
# -------------------------------------------------
niche = sys.argv[1]          # ex. "jardin vertical indoor"
title_prompt = f"Give me a catchy French blog title about {niche} (max 70 chars)."
title = hf_generate(title_prompt).strip()
slug = slugify(title)

# -------------------------------------------------
#  2️⃣  Générer le corps de l’article (≈ 2000 mots)
# -------------------------------------------------
article_prompt = (
    f"Write a 2000‑word SEO‑friendly French article titled \"{title}\". "
    "Include an introduction, four H2 sections (pros, cons, buying guide, FAQ), "
    "and a short conclusion. Use bullet points where appropriate."
)
article = hf_generate(article_prompt, max_new_tokens=1500)

# -------------------------------------------------
#  3️⃣  Sauvegarder le markdown dans le dossier _posts/
# -------------------------------------------------
date = datetime.date.today().isoformat()
front_matter = textwrap.dedent(f"""\
    ---
    title: "{title}"
    date: {date}
    slug: {slug}
    categories: [{niche}]
    tags: ["affiliation","{niche}"]
    ---
    """)

content = front_matter + "\n" + article
os.makedirs("_posts", exist_ok=True)
path = f"_posts/{date}-{slug}.md"
with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"✅ {path} créé")
