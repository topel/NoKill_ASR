# Trancription automatique de la parole

Ce dossier regroupe les codes écrits lors de mon stage réalisé de juin à septembre 2019  à l'Institut de Recherche en Informatique de Toulouse (IRIT) dont l'objectif etait de réaliser un système de reconnaissance automatique de la parole aui serait utilisé pour une pièce de théâtre par la compagnie No Kill (http://cienokill.fr/spectacles/turing-test/).
Lors de ce stage, deux approches ont été développées : la première est l'utilisation de l'API Speech To Text développée par Google, la seconde est l'utilisation de  modèles développés à l'IRIT.

Le dossier **Google_API** regroupe les scripts python permettant de porcéder a la reconaissance automatique de la parole en utilisant l'API Google. Deux scripts sont fournis : 
* Le premier permet de faire la transcription de l'audio en streaming en utilisant comme source audio le micro de l'ordinateur 
* Le second permet de faire la transcription d'un fichier audio au format wav

Le dossier **IRIT_model** regroupe les scripts python, bash et perl permettant de :
* Créer un corpus textuel basé sur du contenu Wikipédia
* Entrainer un modèle de langage à partir de différents corpus textuels
* Générer un graphe de transcription en utilisant kaldi
* Effectuer la reconnaissance automatique de la parole en utilisant le graphe généré


## Prérequis

Il est recommandé Ubuntu. La liste des installations nécessaire peut être incomplète.

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

## Licence
Certains scripts sont basés sur le travail réalisé par d'autres. Merci de regarder les entêtes des fichiers pour plus d'information.
