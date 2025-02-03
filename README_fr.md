# YtbSon

YouTube Audio Downloader and Converter (actuellement obsolète)

## Introduction

À force d'avoir recours à des sites internet douteux pour obtenir les pistes audio des vidéos YouTube, je me suis demandé s'il était possible de programmer soi-même son convertisseur. Tout l'intérêt de ce projet est de créer un convertisseur simple et efficace qui n'impose pas de publicités, de redirections, de délais ou de clics inutiles.

Intéressons-nous au fonctionnement de YouTube. Le fichier audio extrait d'une vidéo est initialement dans le format fourni par YouTube (souvent WebM ou MP4). Le format  WebM est un simple format de compression avec perte tandis que le MP4 est un conteneur, c'est-à-dire qu'il peut contenir plusieurs pistes audio ou vidéo de formats différents (par exemple : MP3 ou AAC). Le format AAC, ne contenant pas de métadonnées, ne me convient pas, donc nous devons le convertir. Nous proposons deux formats de conversion : FLAC (sans perte) et MP3 (avec perte), qui sont très répandus. La bibliothèque Python `pytubefix` permet de récupérer des vidéos YouTube. La conversion se fait depuis le terminal et, pour ne pas ajouter de paramètres supplémentaires, nous avons un script pour chaque format : `ytbmp3.py` et `ytbflac.py`. 

Notez que la conversion en MP3 diminue la qualité audio car c'est un format de compression avec perte. Les fichiers FLCAC sont en moyenne dix fois plus volumineux pour des musiques mais ne perdent pas en qualité (comparés au fichier extrait de la vidéo YouTube). La qualité d'un format MP3 est notamment liée à sont débit binaire en kb/s. Malgrès que la qualité ne pourra être améliorée, elle pourrait être fortement diminuée si ce paramêtre est trop faible. Il doit donc être correctement ajusté.

## Prérequis

- Python 3.x (<https://www.python.org/>)
- Les bibliothèques suivantes :
  - `pytubefix`
  - (pour `ytbmp3.py`) `pydub`
  - `mutagen`
- (pour `ytbflac.py`) `ffmpeg` installé et accessible dans le PATH système

### Installation des Prérequis

Après avoir installé Python. Dont les commandes suivantes permettent de vérifier que tout est bon

> python --version
> pip --version

Installez les bibliothèques Python nécessaires depuis votre terminal avec la commande :

> pip install pytubefix pydub mutagen

### Installation de ffmpeg

1. Téléchargez `ffmpeg` (<https://ffmpeg.org/download.html>). Sous "Windows", cliquez sur "Windows builds from gyan.dev" et téléchargez une version "release full".
2. Extrayez l'archive téléchargée dans un dossier de votre choix.
3. Ajoutez le chemin du dossier `bin` à la variable d'environnement PATH :
   - Ouvrez les Paramètres système avancés (Win + R, puis entrez "sysdm.cpl") et cliquez sur "Variables d'environnement".
   - Dans la section "Variables utilisateur", modifiez la variable "Path" :
     - Cliquez sur "Nouveau" et ajoutez le chemin complet vers le dossier `bin` du répertoire de `ffmpeg` (par exemple, `C:\user\ffmpeg\bin`). Cliquez sur "OK".
   - Vérifiez avec la commande `ffmpeg -version` dans votre terminal.


## Utilisation

### ytbflac.py

Exécutez la commande suivante dans votre terminal (positionné dans le répartoire du script) :

> python ytbflac.py <URL_de_la_vidéo_YouTube> [chemin_de_sortie]

- `<URL_de_la_vidéo_YouTube>` : L'URL de la vidéo YouTube que vous souhaitez télécharger.
- `[chemin_de_sortie]` : (Optionnel) Le répertoire où le fichier audio sera enregistré. Si aucun chemin n'est spécifié, le fichier sera enregistré dans le répertoire Downloads de l'utilisateur.

**Exemple**

Pour télécharger et convertir une vidéo YouTube en FLAC et enregistrer le fichier dans le répertoire Downloads, utilisez la commande suivante :

> python ytbflac.py https://www.youtube.com/watch?v=dQw4w9WgXcQ

**Fonctionnalités**

- Convertit le flux audio téléchargé en format FLAC.
- Ajoute des métadonnées (titre, auteur) au fichier FLAC.
- Supprime le fichier audio original après conversion.

**Notes**

- Le fichier audio téléchargé est initialement dans le format fourni par YouTube (souvent WebM ou MP4). Le format MP4 est un conteneur et peut contenir plusieurs pistes audio ou vidéo de formats différents (ex : AAC, mais ce format audio ne permet pas de conserver des métadonnées).
- Le script convertit automatiquement les fichiers WebM et MP4 en FLAC à l'aide de `ffmpeg` (plus rapide que `pydub`).

### ytbmp3.py

Exécutez la commande suivante dans votre terminal :

> python ytbmp3.py <URL_de_la_vidéo_YouTube> [chemin_de_sortie] --bitrate [bitrate]


- `<URL_de_la_vidéo_YouTube>` : L'URL de la vidéo YouTube que vous souhaitez télécharger.
- `[chemin_de_sortie]` : (Optionnel) Le répertoire où le fichier audio sera enregistré. Si aucun chemin n'est spécifié, le fichier sera enregistré dans le répertoire Downloads de l'utilisateur.
- `[bitrate]` : (Optionnel) La valeur du débit binaire en kbps. Par défaut, elle est de 124 kbps.

**Exemple**

Pour télécharger et convertir une vidéo YouTube en MP3 et enregistrer le fichier dans le répertoire Downloads en vous situant dans le répertoire du script, utilisez la commande suivante :

> python ytbmp3.py https://www.youtube.com/watch?v=bc0KhhjJP98


Pour sélectionner un débit binaire de 320 kbps :

> python ytbmp3.py https://www.youtube.com/watch?v=aqRGb8JkO38 --bitrate 320


**Fonctionnalités**

- Convertit le flux audio téléchargé en format MP3.
- Ajoute des métadonnées (titre, auteur) au fichier MP3.

**Notes**

- Le script convertit automatiquement les fichiers WebM et MP4 en MP3 à l'aide de `pydub` (plus lent que `ffmpeg`).
- La qualité finale de la piste audio ne peut excéder celle de la piste extraite de la page web. Un haut débit binaire approche la qualité originale, mais consomme plus d'espace (moins qu'un fichier FLAC), tandis qu'un débit binaire faible détériore significativement la qualité audio.


-------------------------------------------------
## Contribution

Merci à Gauthier MARTIN pour ses conseils.

Camille ANSEL
