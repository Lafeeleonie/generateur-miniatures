# Générateur de miniatures / Thumbnail generator

## Français

Petit programme Tkinter qui crée une miniature PNG à partir d’un fond présent dans `fond/`, puis prépare le titre et la description d’une vidéo YouTube.

### Lancer le programme

Double-cliquez sur `creer_miniature.bat`. Le script crée automatiquement l’environnement virtuel et installe Pillow lors du premier lancement.

### Configuration

- `donnee.json` contient les classes disponibles, la classe sélectionnée, le dernier niveau de clé utilisé, les couleurs et les liens de description.
- `donjon.json` associe directement le nom exact d’un fichier de fond à son nom de donjon affiché. Pour ajouter ou renommer un donjon, modifiez ce fichier et placez le fond correspondant dans `fond/`.
- Les fonds PNG et les miniatures générées ne sont pas suivis par Git.

La miniature est enregistrée à la racine du projet avec le préfixe `zz_`, afin d’apparaître à la fin du dossier. Son nom suit le format `zz_classe_niveau_donjon_miniature.png`.

## English

Small Tkinter application that creates a PNG thumbnail from a background stored in `fond/`, and prepares a YouTube video title and description.

### Running the application

Double-click `creer_miniature.bat`. The script automatically creates the virtual environment and installs Pillow on the first run.

### Configuration

- `donnee.json` contains the available classes, the selected class, the last key level used, the colors, and the description links.
- `donjon.json` directly maps the exact name of a background file to its displayed dungeon name. To add or rename a dungeon, edit this file and place the matching background in `fond/`.
- PNG backgrounds and generated thumbnails are ignored by Git.

The thumbnail is saved at the project root with the `zz_` prefix so it appears at the end of the folder. Its name follows the `zz_class_level_dungeon_miniature.png` format.
