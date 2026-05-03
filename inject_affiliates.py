#!/usr/bin/env python3
import glob, re

# -------------------------------------------------
#  ⚡️  Remplacez les valeurs ci‑dessous par VOS liens d’affiliation réels.
# -------------------------------------------------
AFFILIATE = {
    # Exemple : le texte exact que vous utilisez dans vos articles.
    "kit de jardin vertical hydroponique 30 plantes": "https://amzn.to/EXAMPLE1",
    "tour hydroponique indoor 5 plantes":           "https://amzn.to/EXAMPLE2",
    # Si vous avez un programme Awin / CJ, ajoutez‑les ici.
    "Garden Tower 2":                              "https://www.awin.com/track?clickid=XXXXX&pubid=YOUR_ID",
    "VertiGrow Tower":                            "https://vertigrow.io/aff?ref=YOURCODE",
}

def add_links(text: str) -> str:
    """Remplace chaque occurrence du mot‑clé par un lien Markdown."""
    for kw, url in AFFILIATE.items():
        pattern = r"\b(" + re.escape(kw) + r")\b"
        text = re.sub(pattern, f'[{kw}]({url})', text, flags=re.IGNORECASE)
    return text

# Parcours tous les fichiers markdown générés dans _posts/
for md_path in glob.glob("_posts/*.md"):
    with open(md_path, "r+", encoding="utf-8") as f:
        raw = f.read()
        f.seek(0)
        f.write(add_links(raw))
        f.truncate()
