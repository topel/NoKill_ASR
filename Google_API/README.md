# API Google Speech to Text

Avant de lancer les scripts de transcriptions utilisant l'API Google, il est nécessaire de créer un fichier JSON permettant de s'identifier auprès de Google (https://cloud.google.com/video-intelligence/docs/common/auth?hl=fr). Dans les scripts il est nécessaire de modifier la ligne suivante en précisant le chemin vers le fichier JSON téléchargé depuis Google Cloud :
```python
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="<your_key>.json"
```

Une fois le chemin vers le fichier JSON établi, il suffit de lancer les scripts de la manière suivante pour une transcription en streamming :
```bash
python3 ASR_Google_stream.py
```

ou de cette façon pour une transcription a partir d'un fichier wav :
```bash
python3 ASR_synchronous.py <file_name> <out_path> <transcription_name>
```

Le script python de la transcription d'un fichier wav permet l'enregistrement d'un fichier au format texte contenant la transcription
