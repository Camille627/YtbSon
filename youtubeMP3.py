import argparse
from pytubefix import YouTube
from pydub import AudioSegment
import os

def download_youtube_video_as_mp3(url, output_path):
    try:
        # Téléchargement de la vidéo YouTube
        yt = YouTube(url)
        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=output_path)

        # Conversion du fichier vidéo en MP3
        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        audio = AudioSegment.from_file(out_file)
        audio.export(new_file, format='mp3')
        
        # Suppression du fichier vidéo original
        os.remove(out_file)

        print(f"Conversion réussie ! Fichier MP3 enregistré à : {new_file}")
    except Exception as e:
        print(f"Erreur lors du téléchargement: {e}")

def main():
    parser = argparse.ArgumentParser(description='Télécharger une vidéo YouTube et la convertir en MP3.')
    parser.add_argument('url', type=str, help='URL de la vidéo YouTube')
    parser.add_argument('output_path', type=str, help='Répertoire de destination pour le fichier MP3')

    args = parser.parse_args()

    # Utiliser le répertoire "Téléchargements" par défaut si le chemin de sortie est une chaîne vide
    if args.output_path == "dl":
        args.output_path = os.path.join(os.path.expanduser('~'), 'Downloads')
	
    download_youtube_video_as_mp3(args.url, args.output_path)

if __name__ == '__main__':
    main()
