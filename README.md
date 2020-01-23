# NaturalLanguageProcessing_ESGI_5IABD_S1

## Utiliser l'environnement conda du Plugin/API
- Aller à la racine du projet
- Lancer la commande `conda env create -f conda_env/env_nlp.yaml`
- Lancer la commande `conda activate env_nlp`

## Test du Plugin/API
- Ouvrir un terminal
- Activer l'environnement `conda activate env_nlp`
- Aller dans le dossier Scraper `cd /real/path/project/scraper`
- Lancer la commande `python quick_termofuse_api.py`
- Ouvrir l'application `google chrome`
- Dans l'url écrire `chrome://extensions/`
- Activer `Developer mode` (en haut a droite dans mon cas)
- Ensuite vous devriez avoir le bouton `Load unpacked` qui apparait
- Selectionner le dossier `plugin_chrome`
- Puis aller sur un la parti CGU ou cookie d'un site (example : http://mentions-legales.lefigaro.fr/page/cgu)
- cliquer sur le bouton `Check this website now!`

Pour le moment le plugin/API fonctionne seulement en local, il faut 2 semaines de validation pour pouvoir en publier un.

## Comprendre les fichiers importants
- `../project/conda_env/env_nlp_v2.yaml` contient l'ensemble des packages nécéssaires à t'utilisation de l'API.
- `../project/modele/Aargan/check_important_word_in_sentences.py` et `../project/modele/Aargan/check_important_word_in_sentences_en.py` permettent de contener les occurances des mots au sein d'un corpus et de condencer les corpus. En entré il prend l'ensemble de nos corpus.Deux fichiers en sortie : CGU_{FR/EN}.text et top_word.{_en}txt.
- `../project/modele/Aargan/Text_Summarization_Fr.ipynb` Permet de comprendre les principes utilé afin de résumé utilisé le texte.
- `../project/modele/Chanez/GloVe-master/demo2.sh` Permet de créer notre dictionnaire de vecteur. En entré il prend : CGU_{FR/EN}.text et top_word.{_en}txt. En sortie nous utiliseront le fichier vectors{_en}.txt.
- `../project/scraper/quick_termofuse_api.py` C'est le coeur du projet, l'API.