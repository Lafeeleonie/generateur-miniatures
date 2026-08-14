import json
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

# Lecture des donnees
dossier = Path(__file__).resolve().parent
with open(dossier / "donnee.json", encoding="utf-8") as fichier_json:
    donnees = json.load(fichier_json)

# Variables simples, toutes issues du JSON
classe = donnees["classe"]
cle = donnees["cle"]
police = donnees["police"]
taille_titre = donnees["taille_titre"]
taille_sous_titre = donnees["taille_sous_titre"]
violet_principal = donnees["violet_principal"]
violet_sombre = donnees["violet_sombre"]
violet_contour = donnees["violet_contour"]
noir = donnees["noir"]
blanc = donnees["blanc"]

# Reglages simples de positionnement : a modifier librement ici
marge_haut = 600
marge_bas = 80
marge_cote = 60
epaisseur_contour = 4

# Texte cree a partir des donnees du JSON
titre = f"{classe}  —  M+ {cle}"

# Le script prend le seul PNG source du dossier et ignore les miniatures deja creees.
liste_png = [
    fichier for fichier in dossier.glob("*.png")
    if not fichier.name.lower().endswith("_miniature.png")
]
if len(liste_png) != 1:
    raise RuntimeError("Placez exactement un PNG source dans ce dossier.")

image_source = liste_png[0]
image = Image.open(image_source).convert("RGBA")
dessin = ImageDraw.Draw(image)

# La police doit etre posee dans le dossier avec le script : Morpheus.ttf ou Morpheus.otf.
fichier_ttf = dossier / f"{police}.ttf"
fichier_otf = dossier / f"{police}.otf"
if fichier_ttf.is_file():
    fichier_police = fichier_ttf
elif fichier_otf.is_file():
    fichier_police = fichier_otf
else:
    raise FileNotFoundError(f"Police introuvable : ajoutez {police}.ttf dans {dossier}.")

font_titre = ImageFont.truetype(fichier_police, taille_sous_titre)

# Titre centre en haut de l'image
boite_titre = dessin.textbbox((0, 0), titre, font=font_titre, stroke_width=epaisseur_contour)
largeur_titre = boite_titre[2] - boite_titre[0]
x_titre = (image.width - largeur_titre) // 2
y_titre = marge_haut
dessin.text(
    (x_titre, y_titre), titre,
    font=font_titre,
    fill=ImageColor.getrgb(violet_principal),
    stroke_width=epaisseur_contour,
    stroke_fill=ImageColor.getrgb(violet_contour),
)

fichier_sortie = dossier / "xx_miniature.png"
image.save(fichier_sortie)
print(f"Miniature creee : {fichier_sortie.name}")
