# Trancription automatique de la parole

Ce dossier contient le code necessaire pour effectuer de la reconaissance automatique de la parole. Ce dossier à été créé suite à un stage réalisé de juin à septembre 2019  à l'Institut de Recherche en Informatique de Toulouse (IRIT) dont l'objectif etais de réaliser un système de reconnaissance automatique de la parole aui serait utilisé pour une pièce de théâtre par la compagnie No Kill (http://cienokill.fr/spectacles/turing-test/).

Deux approches ont été utilisées : la première est l'utilisation de l'API Speech To Text développée par Google, la seconde est l'utilisation de  modèles développés à l'IRIT.

Les scripts faisant appel à l'API Google permettent directement de faire de la reconaissance.

Les scripts faisant appel aux modèles développés à l'IRIT permet, a partir d'un corpus de textes d'entraîner un modèle de langage et ainsi recréer un graphe de transcription en utilisant kaldi et un modèle acoustique à fournir au modèle.

Le dossier contiens des codes python 2 et 3 permettant d'éffectuer la reconaissance mais aussi de créer un corpus dans le but d'entraîner un modèle de langage, effectuer l'entraînement de ce dernier et de génerer le graphe permettant la reconaissance

## Avant de commencer

Il est recommandé Ubuntu, en effet certains packages nécessaires ne sont disponibles que sur cette plateforme.

### Prérequis

Cette liste peut être incomplète

#### Python 3
Python 3 n'est utilisé que pour l'utilisation de l'API Google. Afin de pouvoir utiliser les scripts présentés, il va falloir installer les packages python 3 suivants :
* pyaudio (https://pypi.org/project/PyAudio/#description)
* pydub (https://pypi.org/project/pydub/)
* google-cloud-speech (https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries#client-libraries-install-python)
* webrtcvad (https://pypi.org/project/webrtcvad/)

#### Python 2
Python 2 est utilisé pour la génération du corpus, l'entrainement du modèle de langage ainsi que la composition du modèle final. Les packages suivants sont requis :
* beautifulsoup (https://pypi.org/project/beautifulsoup4/)
* num2words (https://pypi.org/project/num2words/)
* unidecode (https://pypi.org/project/Unidecode/)
* unicodedata

#### Système
Afin d'entraîner le modèle de langage, il va falloir installer dans un premier temps Kaldi (https://github.com/kaldi-asr/kaldi)
Puis insaller SRILM dans Kaldi. Pour ce faire Télecharger SRILM renomer l,archiive télechargée srilm.tgz et la placer dans le fichier kaldi/tools/ . Enfin, executer le scipt kaldi/tools/install_srilm.sh

Pour effectuer la phonetisation des mots hors vocabulaires, Il est necessaire d'installer Phonetisaurus (https://github.com/AdolfVonKleist/Phonetisaurus#phonetisaurus-g2p)

Certains scripts sont basés sur le travail réalisé par d'autres.  Merci de regarder les entêtes des fichiers pour plus d'information.


