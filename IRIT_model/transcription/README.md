Ce répertoire contient les scripts nécessaires à la reconaissance de parole en utilisant un modèle Kaldi pour différents cas de figure :

* *kaldi_decode_wav.py* : permet de transcrire un fichier wav : 
```bash
python kaldi_decode_wav.py <yourfile.wav>
```

* *file_kaldi_decode_live.py* : permet d'effectuer la reconaissance a partir d'un fichier wav en simulant du streaming
```bash
python file_kaldi_decode_live.py <yourfile.wav>
```

* *kaldi_decode_live.py* : permet d'effectuer la reconaissance en utilisant l'audio du micro
```bash
python kaldi_decode_live.py
```

## Prérequis

Avant de commencer la transcription :
* copier le dossier graph généré précédamment dans le dossier `model/model`. Plusieurs dossiers contenant des graphes peuvent être placés dans ce dossier. Le graphe que l'on souhaite utiliser doit être dans le dossier nomé graph 
* Modifier dans les scripts le chemin d'accès vers le modèle :
```python
DEFAULT_MODEL_DIR = <path_to_the_model_directory>
```
