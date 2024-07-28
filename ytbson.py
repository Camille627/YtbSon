import argparse
import os
import shutil
import subprocess
from pytubefix import YouTube
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4
import json

def get_audio_codec(input_file):
    """
    Obtient le codec audio d'un fichier vidéo.

    Args:
        input_file (str): Chemin du fichier vidéo.

    Returns:
        str: Codec audio utilisé dans le fichier vidéo.
    """
    try:
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'stream=index,codec_type,codec_name', '-of', 'json', input_file], 
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True
        )
        streams = json.loads(result.stdout)['streams']
        for stream in streams:
            if stream['codec_type'] == 'audio':
                return stream['codec_name']
        return None
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'analyse du fichier vidéo : {e}")
        return None

def extract_audio_without_conversion(input_file, output_file, metadata):
    """
    Extrait l'audio d'un fichier vidéo sans conversion et ajoute des métadonnées.

    Args:
        input_file (str): Chemin du fichier vidéo.
        output_file (str): Chemin du fichier audio de sortie.
        metadata (dict): Dictionnaire contenant les métadonnées à ajouter.
    """
    try:
        audio_codec = get_audio_codec(input_file)
        if audio_codec:
            if audio_codec == 'aac':
                command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file + '.aac']
                subprocess.run(command, check=True)
                add_metadata_to_file(output_file + '.aac', metadata, 'aac')
                os.remove(input_file)
            elif audio_codec == 'mp3':
                command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file + '.mp3']
                subprocess.run(command, check=True)
                add_metadata_to_file(output_file + '.mp3', metadata, 'mp3')
                os.remove(input_file)
            elif audio_codec == 'flac':
                command = ['ffmpeg', '-i', input_file, '-vn', '-acodec', 'copy', output_file + '.flac']
                subprocess.run(command, check=True)
                add_metadata_to_file(output_file + '.flac', metadata, 'flac')
                os.remove(input_file)
            else:
                print(f"Codec audio non pris en charge : {audio_codec}")
                return
            print(f"Extraction audio réussie : {output_file}")
        else:
            print("Aucun flux audio trouvé dans le fichier vidéo.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'extraction audio : {e}")

def convert_webm_to_flac(webm_file, flac_file, metadata):
    """
    Convertit un fichier WebM en FLAC et ajoute des métadonnées.

    Args:
        webm_file (str): Chemin du fichier WebM.
        flac_file (str): Chemin du fichier de sortie FLAC.
        metadata (dict): Dictionnaire contenant les métadonnées à ajouter.
    """
    try:
        subprocess.run(['ffmpeg', '-i', webm_file, flac_file], check=True)
        add_metadata_to_file(flac_file, metadata, 'flac')
        os.remove(webm_file)
        print(f"Conversion réussie : {flac_file}")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de la conversion de WebM en FLAC : {e}")

def add_metadata_to_file(audio_file, metadata, file_type):
    """
    Ajoute des métadonnées au fichier audio.

    Args:
        audio_file (str): Chemin du fichier audio.
        metadata (dict): Dictionnaire contenant les métadonnées à ajouter.
        file_type (str): Type du fichier audio (aac, mp3, flac).
    """
    try:
        if file_type == 'mp3':
            audio = EasyID3(audio_file)
        elif file_type == 'flac':
            audio = FLAC(audio_file)
        elif file_type == 'aac':
            audio = MP4(audio_file)
        else:
            print(f"Type de fichier non pris en charge pour les métadonnées : {file_type}")
            return

        if 'title' in metadata:
            audio['title'] = metadata['title']
        if 'artist' in metadata:
            audio['artist'] = metadata['artist']
        if 'album' in metadata:
            audio['album'] = metadata['album']
        audio.save()
        print(f"Métadonnées ajoutées à : {audio_file}")
    except Exception as e:
        print(f"Erreur lors de l'ajout des métadonnées : {e}")

def download_youtube_video_as_audio(url, output_path):
    """
    Télécharge une vidéo YouTube, extrait l'audio et le convertit en FLAC si le format est WebM,
    ou extrait l'audio sans conversion si le format est MP4.

    Args:
        url (str): L'URL de la vidéo YouTube.
        output_path (str): Le répertoire où le fichier audio sera enregistré.
    """
    try:
        # Crée un objet YouTube
        yt = YouTube(url)
        
        # Sélectionne le flux audio de la meilleure qualité disponible
        video = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
        
        # Télécharge le flux audio
        out_file = video.download(output_path=output_path)
        
        # Récupère les métadonnées
        metadata = {
            'title': yt.title,
            'artist': yt.author,
            'album': 'YouTube'
        }

        # Vérifie le format du fichier et procède en conséquence
        base, ext = os.path.splitext(out_file)
        if ext.lower() == '.webm':
            flac_file = f"{base}.flac"
            convert_webm_to_flac(out_file, flac_file, metadata)
            print(f"Fichier WebM converti en FLAC : {flac_file}")
        elif ext.lower() == '.mp4':
            output_file_base = os.path.splitext(out_file)[0]
            extract_audio_without_conversion(out_file, output_file_base, metadata)
        else:
            print(f"Format de fichier non pris en charge : {ext}")

    except Exception as e:
        print(f"Erreur : {e}")

def main():
    """
    Point d'entrée principal du script. Parse les arguments de la ligne de commande
    et appelle la fonction de téléchargement et de conversion.
    """
    parser = argparse.ArgumentParser(description='Télécharger une vidéo YouTube et la convertir en audio.')
    parser.add_argument('url', type=str, help='URL de la vidéo YouTube')
    parser.add_argument('output_path', type=str, nargs='?', default='', help='Répertoire de destination pour le fichier audio')

    args = parser.parse_args()

    # Utilise le répertoire "Downloads" par défaut si aucun répertoire de destination n'est spécifié
    if args.output_path == '':
        args.output_path = os.path.join(os.path.expanduser('~'), 'Downloads')

    download_youtube_video_as_audio(args.url, args.output_path)

if __name__ == '__main__':
    main()
