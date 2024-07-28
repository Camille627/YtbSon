import argparse
import os
import shutil
import subprocess
from pytubefix import YouTube
from pydub import AudioSegment
from mutagen.easyid3 import EasyID3

def get_video_metadata(url):
    """
    Récupère les métadonnées d'une vidéo YouTube.

    Args:
        url (str): L'URL de la vidéo YouTube.

    Returns:
        dict: Un dictionnaire contenant le titre et l'auteur de la vidéo.
        None: Si une erreur survient lors de la récupération des métadonnées.
    """
    try:
        yt = YouTube(url)
        metadata = {
            'title': yt.title,
            'author': yt.author
        }
        return metadata
    except Exception as e:
        print(f"Erreur de récupération des métadonnées: {e}")
        return None

def check_audio_bitrate(file_path):
    """
    Vérifie le débit binaire réel du fichier audio à l'aide de ffmpeg.

    Args:
        file_path (str): Le chemin du fichier audio.

    Returns:
        int: Le débit binaire réel en kbps.
    """
    try:
        result = subprocess.run(
            ['ffmpeg', '-i', file_path],
            stderr=subprocess.PIPE,
            universal_newlines=True
        )
        for line in result.stderr.split('\n'):
            if 'Stream #0:0' in line and 'Audio' in line:
                parts = line.split(',')
                for part in parts:
                    if 'kb/s' in part:
                        return int(part.strip().split(' ')[0])
    except Exception as e:
        print(f"Erreur lors de la vérification du débit binaire : {e}")
    return None

def download_youtube_video_as_mp3(url, output_path):
    """
    Télécharge une vidéo YouTube, extrait l'audio et le convertit en MP3.

    Args:
        url (str): L'URL de la vidéo YouTube.
        output_path (str): Le répertoire où le fichier MP3 sera enregistré.
    """
    try:
        # Crée un objet YouTube
        yt = YouTube(url)
        
        # Sélectionne le flux audio de la meilleure qualité disponible
        video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        # Télécharge le flux audio
        out_file = video.download(output_path=output_path)

        # Récupère le débit binaire (abr) du flux audio
        bitrate = video.abr

        # Sauvegarde et renomme le fichier audio original
        base, ext = os.path.splitext(out_file)
        original_audio_file = f"{base}_copie{ext}"
        shutil.copy(out_file, original_audio_file)
        print(f"Fichier audio original sauvegardé à : {original_audio_file}")

        # Vérifie le débit binaire réel du fichier téléchargé
        real_bitrate = check_audio_bitrate(out_file)
        print(f"Débit binaire réel du fichier audio téléchargé : {real_bitrate} kbps (attendu : {expected_bitrate})")

        # Convertit le fichier audio en MP3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        audio = AudioSegment.from_file(out_file)
        audio.export(new_file, format='mp3')
        
        # Supprime le fichier audio original
        os.remove(out_file)

        # Récupère les métadonnées de la vidéo
        metadata = get_video_metadata(url)
        if metadata:
            # Ajoute les métadonnées au fichier MP3
            add_metadata(new_file, metadata['title'], metadata['author'], "YouTube")
        else:
            print("Aucune métadonnée récupérée.")

        print(f"Conversion réussie ! Fichier MP3 enregistré à : {new_file}")
        print(f"Débit binaire du flux audio : {bitrate}")
    except Exception as e:
        print(f"Erreur : {e}")

def add_metadata(mp3_file, title, artist, album):
    """
    Ajoute des métadonnées au fichier MP3.

    Args:
        mp3_file (str): Le chemin du fichier MP3.
        title (str): Le titre de la chanson.
        artist (str): L'artiste de la chanson.
        album (str): L'album de la chanson.
    """
    try:
        audio = EasyID3(mp3_file)
        audio['title'] = title
        audio['artist'] = artist
        audio['album'] = album
        audio.save()
    except Exception as e:
        print(f"Erreur lors de l'ajout des métadonnées : {e}")

def main():
    """
    Point d'entrée principal du script. Parse les arguments de la ligne de commande
    et appelle la fonction de téléchargement et de conversion.
    """
    parser = argparse.ArgumentParser(description='Télécharger une vidéo YouTube et la convertir en MP3.')
    parser.add_argument('url', type=str, help='URL de la vidéo YouTube')
    parser.add_argument('output_path', type=str, nargs='?', default='', help='Répertoire de destination pour le fichier MP3')

    args = parser.parse_args()

    # Utilise le répertoire "Downloads" par défaut si aucun répertoire de destination n'est spécifié
    if args.output_path == '':
        args.output_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    download_youtube_video_as_mp3(args.url, args.output_path)

if __name__ == '__main__':
    main()
