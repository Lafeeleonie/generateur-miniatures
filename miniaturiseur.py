"""Crée une miniature PNG en utilisant les paramètres de donnee.json."""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageColor, ImageDraw, ImageFont

RACINE = Path(__file__).resolve().parent
FICHIERS_A_IGNORER = {"xx_miniature.png"}


def couleur(valeur: str) -> tuple[int, int, int, int]:
    """Convertit une couleur HTML du JSON en couleur Pillow RGBA."""
    return (*ImageColor.getrgb(valeur), 255)


def trouver_image() -> Path:
    images = [
        chemin for chemin in RACINE.glob("*.png")
        if chemin.name.lower() not in FICHIERS_A_IGNORER
        and not chemin.name.lower().endswith("_miniature.png")
    ]
    if len(images) != 1:
        raise RuntimeError(
            "Placez exactement un PNG source dans ce dossier "
            "(les fichiers *_miniature.png sont ignorés)."
        )
    return images[0]


def charger_police(nom: str, taille: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidats = [RACINE / f"{nom}.ttf", RACINE / f"{nom}.otf"]
    candidats.extend([Path("C:/Windows/Fonts/arialbd.ttf"), Path("C:/Windows/Fonts/arial.ttf")])
    for chemin in candidats:
        if chemin.is_file():
            return ImageFont.truetype(str(chemin), taille)
    return ImageFont.load_default()


def adapter_taille(draw: ImageDraw.ImageDraw, texte: str, police: ImageFont.FreeTypeFont | ImageFont.ImageFont,
                    largeur_max: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    if not isinstance(police, ImageFont.FreeTypeFont):
        return police
    taille = police.size
    while taille > 20 and draw.textbbox((0, 0), texte, font=police, stroke_width=2)[2] > largeur_max:
        taille -= 4
        police = charger_police("Morpheus", taille)
    return police


def main() -> None:
    parser = argparse.ArgumentParser(description="Ajoute un titre à la miniature PNG.")
    parser.add_argument("--sortie", default="xx_miniature.png", help="Nom du PNG créé.")
    parser.add_argument("--titre", help="Titre à afficher (par défaut : classe + clé du JSON).")
    args = parser.parse_args()

    with (RACINE / "donnee.json").open(encoding="utf-8") as fichier:
        donnees = json.load(fichier)

    titre = args.titre or f"{donnees['classe']} - +{donnees['cle']}"
    source = trouver_image()
    image = Image.open(source).convert("RGBA")
    dessin = ImageDraw.Draw(image)
    police = charger_police(donnees.get("police", "Morpheus"), int(donnees["taille_titre"]))
    police = adapter_taille(dessin, titre, police, image.width - 120)

    boite = dessin.textbbox((0, 0), titre, font=police, stroke_width=4)
    x = (image.width - (boite[2] - boite[0])) // 2
    y = image.height - (boite[3] - boite[1]) - 80
    dessin.text((x, y), titre, font=police, fill=couleur(donnees["blanc"]),
                stroke_width=8, stroke_fill=couleur(donnees["noir"]))
    image.save(RACINE / args.sortie)
    print(f"Miniature créée : {args.sortie} (source : {source.name}, titre : {titre})")


if __name__ == "__main__":
    main()
