Album Souvenirs
---------------
Application Flask qui permet de créer un album photos à partir d’un fichier ZIP et d’une photo de profil, avec lecture musicale en boucle.
Architecture hybride :

 -----------------------------------------------------------
 Frontend (Page 1) : statique (GitHub Pages) ou servi par Flask 
 -----------------------------------------------------------
 Backend (Page 2 + upload + extraction ZIP) : Flask (Render)    
 -----------------------------------------------------------

Fonctionnalités
---------------
Page 1 : formulaire (titre d’album, choix musique, photo profil, ZIP d’images) + vidéo descriptive

Page 2 : affichage dynamique de l’album (4 par 4, rotation auto), contrôles musique (play/pause/stop), boutons next/prev et retour

- Nettoyage contrôlé des données (vider_les_donnees()), pour éviter les conflits

- Sélecteur de musiques depuis static/audio_sounds/

- Compatible desktop et mobile (responsive)


