import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageColor, ImageDraw, ImageFont


DOSSIER_PROGRAMME = Path(__file__).resolve().parent
DOSSIER_RACINE = DOSSIER_PROGRAMME.parent
DOSSIER_FONDS = DOSSIER_RACINE / "fond"
NOMS_CLASSES = {"BDK": "Blood DK"}


def charger_donnees():
    with open(DOSSIER_RACINE / "donnee.json", encoding="utf-8") as fichier_json:
        return json.load(fichier_json)


def charger_donjons():
    with open(DOSSIER_RACINE / "donjon.json", encoding="utf-8") as fichier_json:
        return json.load(fichier_json)


def sauvegarder_donnees(donnees):
    with open(DOSSIER_RACINE / "donnee.json", "w", encoding="utf-8") as fichier_json:
        json.dump(donnees, fichier_json, ensure_ascii=False, indent=2)
        fichier_json.write("\n")


def charger_police(donnees):
    nom_police = donnees["police"]
    for extension in (".ttf", ".otf"):
        fichier_police = DOSSIER_PROGRAMME / f"{nom_police}{extension}"
        if fichier_police.is_file():
            return ImageFont.truetype(fichier_police, donnees["taille_sous_titre"])
    raise FileNotFoundError(
        f"Police introuvable : ajoutez {nom_police}.ttf ou {nom_police}.otf dans {DOSSIER_PROGRAMME}."
    )


def creer_miniature(fond, donnees, police):
    image = Image.open(fond).convert("RGBA")
    dessin = ImageDraw.Draw(image)
    titre = f'{donnees["classe"]}  —  M+ {donnees["cle"]}'
    epaisseur_contour = 4

    boite_titre = dessin.textbbox((0, 0), titre, font=police, stroke_width=epaisseur_contour)
    largeur_titre = boite_titre[2] - boite_titre[0]
    x_titre = (image.width - largeur_titre) // 2
    dessin.text(
        (x_titre, 600),
        titre,
        font=police,
        fill=ImageColor.getrgb(donnees["violet_principal"]),
        stroke_width=epaisseur_contour,
        stroke_fill=ImageColor.getrgb(donnees["violet_contour"]),
    )

    nom_classe = donnees["classe"].lower()
    fichier_sortie = DOSSIER_RACINE / f"zz_{nom_classe}_{donnees['cle']}_{fond.stem}_miniature.png"
    image.save(fichier_sortie)
    return fichier_sortie


def titre_video(fond, donnees, noms_donjons=None):
    if noms_donjons is None:
        noms_donjons = charger_donjons()
    nom_donjon = noms_donjons.get(fond.name, fond.stem.replace("_", " ").title())
    nom_classe = NOMS_CLASSES.get(donnees["classe"], donnees["classe"])
    return f'{nom_donjon} +{donnees["cle"]} | {nom_classe} Tank POV | WoW Midnight M+'


def description_video(donnees):
    liens_personnages = donnees.get("liens_personnages", {})
    lien_personnage = liens_personnages.get(donnees["classe"], "")
    liens_communs = donnees.get("liens_communs", [])

    if isinstance(liens_communs, str):
        liens_communs = liens_communs.split(",")

    if not liens_personnages and not liens_communs:
        liens = donnees.get("lien_description", donnees.get("lien_desctiption", ""))
        return "\n".join(lien.strip() for lien in liens.split(",") if lien.strip())

    return "\n".join(
        lien.strip()
        for lien in [lien_personnage, *liens_communs]
        if lien and lien.strip()
    )


class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Générateur de miniatures")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")
        donnees_initiales = charger_donnees()
        self.noms_donjons = charger_donjons()
        classes = donnees_initiales.get("classe", [])
        if isinstance(classes, str):
            classes = [classes]
        self.classes = classes
        classe_selectionnee = donnees_initiales.get("classe_selectionnee", classes[0] if classes else "")
        self.fonds = sorted(DOSSIER_FONDS.glob("*.png"))
        self.fond_selectionne = tk.StringVar()
        self.classe_selectionnee = tk.StringVar(value=classe_selectionnee)

        cadre = tk.Frame(self, padx=18, pady=18, bg="#1e1e1e")
        cadre.pack()
        tk.Label(
            cadre, text="Classe", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#f0f0f0"
        ).pack(anchor="w")
        cadre_classes = tk.Frame(cadre, bg="#1e1e1e")
        cadre_classes.pack(anchor="w")
        for classe in classes:
            tk.Radiobutton(
                cadre_classes,
                text=classe,
                variable=self.classe_selectionnee,
                value=classe,
                command=self.actualiser_textes,
                bg="#1e1e1e",
                fg="#f0f0f0",
                activebackground="#1e1e1e",
                activeforeground="#ffffff",
                selectcolor="#3a3a3a",
            ).pack(side="left", padx=(0, 12))

        tk.Label(cadre, text="Niveau de clé", font=("Segoe UI", 10, "bold"), bg="#1e1e1e", fg="#f0f0f0").pack(
            anchor="w", pady=(10, 0)
        )
        self.cle = tk.StringVar(value="1")
        self.entree_cle = tk.Spinbox(
            cadre,
            from_=1,
            to=40,
            width=5,
            textvariable=self.cle,
            bg="#2d2d2d",
            fg="#f0f0f0",
            insertbackground="#f0f0f0",
        )
        self.entree_cle.pack(anchor="w")
        self.cle.trace_add("write", lambda *_: self.actualiser_titre())

        tk.Label(
            cadre, text="Donjon", font=("Segoe UI", 12, "bold"), bg="#1e1e1e", fg="#f0f0f0"
        ).pack(anchor="w")

        for fond in self.fonds:
            tk.Radiobutton(
                cadre,
                text=self.noms_donjons.get(fond.name, fond.stem.replace("_", " ").title()),
                variable=self.fond_selectionne,
                value=fond.name,
                command=self.actualiser_textes,
                bg="#1e1e1e",
                fg="#f0f0f0",
                activebackground="#1e1e1e",
                activeforeground="#ffffff",
                selectcolor="#3a3a3a",
            ).pack(anchor="w")

        tk.Label(cadre, text="Titre YouTube", font=("Segoe UI", 10, "bold"), bg="#1e1e1e", fg="#f0f0f0").pack(
            anchor="w", pady=(14, 0)
        )
        cadre_titre = tk.Frame(cadre, bg="#1e1e1e")
        cadre_titre.pack(fill="x")
        self.titre = tk.Entry(cadre_titre, width=64, bg="#2d2d2d", fg="#f0f0f0", insertbackground="#f0f0f0")
        self.titre.pack(side="left", fill="x", expand=True)
        tk.Button(cadre_titre, text="Copier", command=lambda: self.copier(self.titre.get()), bg="#444444", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff").pack(
            side="left", padx=(6, 0)
        )

        tk.Label(cadre, text="Description", font=("Segoe UI", 10, "bold"), bg="#1e1e1e", fg="#f0f0f0").pack(
            anchor="w", pady=(10, 0)
        )
        cadre_description = tk.Frame(cadre, bg="#1e1e1e")
        cadre_description.pack(fill="x")
        self.description = tk.Text(cadre_description, width=64, height=5, wrap="word", bg="#2d2d2d", fg="#f0f0f0", insertbackground="#f0f0f0")
        self.description.pack(side="left", fill="x", expand=True)
        tk.Button(
            cadre_description, text="Copier", command=lambda: self.copier(self.description.get("1.0", "end-1c")), bg="#444444", fg="#ffffff", activebackground="#555555", activeforeground="#ffffff"
        ).pack(side="left", padx=(6, 0), anchor="n")

        self.bouton = tk.Button(
            cadre, text="Générer la miniature", command=self.generer, padx=12, pady=6, bg="#6e2a8f", fg="#ffffff", activebackground="#8536a9", activeforeground="#ffffff"
        )
        self.bouton.pack(anchor="e", pady=(14, 0))

        if self.fonds:
            self.fond_selectionne.set(self.fonds[0].name)
            self.actualiser_textes()

    def fond_choisi(self):
        return next((fond for fond in self.fonds if fond.name == self.fond_selectionne.get()), None)

    def actualiser_textes(self):
        fond = self.fond_choisi()
        if fond is None:
            return
        try:
            donnees = charger_donnees()
            donnees["classe"] = self.classe_selectionnee.get()
            self.cle.set(str(donnees.get("cle", 1)))
            self.actualiser_titre(donnees, fond)
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return
        self.description.delete("1.0", "end")
        self.description.insert("1.0", description_video(donnees))

    def actualiser_titre(self, donnees=None, fond=None):
        if donnees is None:
            try:
                donnees = charger_donnees()
                donnees["cle"] = self.cle.get()
            except (OSError, tk.TclError, ValueError):
                return
        if fond is None:
            fond = self.fond_choisi()
        if fond is None:
            return
        self.titre.delete(0, "end")
        self.titre.insert(0, titre_video(fond, donnees, self.noms_donjons))

    def copier(self, contenu):
        self.clipboard_clear()
        self.clipboard_append(contenu)
        self.update()

    def generer(self):
        fond = self.fond_choisi()
        if fond is None:
            messagebox.showwarning("Aucun donjon", "Sélectionnez un donjon.")
            return

        try:
            donnees = charger_donnees()
            donnees["classe"] = self.classe_selectionnee.get()
            niveau_cle = int(self.cle.get())
            if not 1 <= niveau_cle <= 40:
                raise ValueError("Le niveau de clé doit être compris entre 1 et 40.")
            donnees["cle"] = niveau_cle
            donnees["classe_selectionnee"] = donnees["classe"]
            police = charger_police(donnees)
            sortie = creer_miniature(fond, donnees, police)
            donnees_a_sauvegarder = donnees.copy()
            donnees_a_sauvegarder["classe"] = self.classes
            sauvegarder_donnees(donnees_a_sauvegarder)
            self.actualiser_titre(donnees, fond)
        except Exception as erreur:
            messagebox.showerror("Erreur", str(erreur))
            return


if __name__ == "__main__":
    if not DOSSIER_FONDS.is_dir():
        raise FileNotFoundError(f"Dossier de fonds introuvable : {DOSSIER_FONDS}")
    Application().mainloop()
