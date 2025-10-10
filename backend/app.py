import os
import shutil
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from utils import extract_zip   
from pathlib import Path


app = Flask(__name__)


BASE_DIR = Path(__file__).resolve().parent          # .../Album_Souvenirs/backend
FRONTEND_DIR = BASE_DIR.parent / "frontend"         # .../Album_Souvenirs/frontend

                                                    # templates/ pour page2, static/ pour assets backend
app.config["UPLOAD_FOLDER"] = str(BASE_DIR / "static" / "uploads")

# CLEAN_ON_INDEX = os.getenv("CLEAN_ON_INDEX", "0") == "1"  # OFF par défaut EN LIGNE
CLEAN_ON_INDEX = 1  # uniquement EN LOCAL. Pour les démos.

def vider_les_donnees():
    # 1) Nettoyer le dossier 'uploads'
    if os.path.exists(app.config["UPLOAD_FOLDER"]):
        for entry in os.listdir(app.config["UPLOAD_FOLDER"]):
            entry_path = os.path.join(app.config["UPLOAD_FOLDER"], entry)
            if os.path.isfile(entry_path):
                os.remove(entry_path)
            else:
                shutil.rmtree(entry_path)
    else:
        os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # 2) Vérifier qu'il n'y ait aucun fichier libre à l'extérieur des dossiers autorisés
    static_root = os.path.join("static")
    allowed_dirs = {"audio_sounds", "img", "uploads"}

    for entry in os.listdir(static_root):
        entry_path = os.path.join(static_root, entry)
        if os.path.isfile(entry_path):
            # Supprimer tout fichier à la racine de 'static'
            os.remove(entry_path)
        elif os.path.isdir(entry_path) and entry not in allowed_dirs:
            # Supprimer tout dossier non autorisé
            shutil.rmtree(entry_path)

@app.route('/favicon.ico')
def favicon():
    return ('', 204)


@app.route("/reset", methods=["POST","GET"])
def reset():
    vider_les_donnees()
    return "OK"

# Une route “fourre-tout” pour les assets :
@app.route("/assets/<path:filename>")
def frontend_assets(filename):
    return send_from_directory(str(FRONTEND_DIR / "assets"), filename)


@app.route('/')
def index():
    if CLEAN_ON_INDEX:
        # Appel de la fonction de nettoyage avant de rendre la page
        vider_les_donnees()
    return send_from_directory(str(FRONTEND_DIR), "index.local.html")


@app.route('/lancer_album', methods=['POST'])
def lancer_album():
    # Préparation du dossier album
    ALBUM_FOLDER = os.path.join(app.config["UPLOAD_FOLDER"], "album")
    os.makedirs(ALBUM_FOLDER, exist_ok=True)
    for filename in os.listdir(ALBUM_FOLDER):
        file_path = os.path.join(ALBUM_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    titre_album = request.form.get('titre_album')
    musique_nom = request.form.get('musique_nom')
    photo_profil = request.files.get('photo_profil')
    album_zip = request.files.get('album_zip')

    if photo_profil:
        profil_path = os.path.join(app.config["UPLOAD_FOLDER"], 'profil.jpg')
        photo_profil.save(profil_path)
    if album_zip:
        zip_filename = secure_filename(album_zip.filename)
        zip_path = os.path.join(app.config["UPLOAD_FOLDER"], zip_filename)
        album_zip.save(zip_path)
        extract_zip(zip_path, ALBUM_FOLDER)
        os.remove(zip_path)

    photos = []
    for root, dirs, files in os.walk(ALBUM_FOLDER):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                rel_dir = os.path.relpath(root, ALBUM_FOLDER)
                rel_path = file if rel_dir == '.' else os.path.join(rel_dir, file)
                photos.append(rel_path.replace("\\", "/"))
    photos.sort()

    return render_template(
        'page2_album.html',
        titre_album=titre_album,
        photos=photos,
        musique_nom=musique_nom
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
