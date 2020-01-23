# NaturalLanguageProcessing_ESGI_5IABD_S1

## Utiliser l'environnement conda du Plugin/API
- Aller à la racine du projet
- Lancer la commande `conda env create -f conda_env/env_nlp.yaml`
- Lancer la commande `conda activate env_nlp`

## Test du Plugin/API
- Ouvrir un terminal
- Activer l'environnement `conda activate env_nlp`
- Aller dans le dossier Scraper `cd /real/path/NaturalLanguageProcessing_ESGI_5IABD_S1/scraper`
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
- `../NaturalLanguageProcessing_ESGI_5IABD_S1/conda_env/env_nlp_v2.yaml` Contient l'ensemble des packages nécéssaires à t'utilisation de l'API.
- `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Aargan/check_important_word_in_sentences.py` et `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Aargan/check_important_word_in_sentences_en.py` Permettent de compter les occurances des mots au sein d'un corpus et de condencer les corpus en un seul fichier. En entré il prend l'ensemble de nos corpus. Deux fichiers en sortie : CGU_{FR/EN}.text et top_word{_en}.txt.
- `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Aargan/Text_Summarization_Fr.ipynb` Permet de comprendre les principes utilisé afin de résumé utilisé le texte.
- `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Chanez/GloVe-master/demo2.sh` Permet de créer notre dictionnaire de vecteur. En entré il prend : CGU_{FR/EN}.text et top_word.{_en}txt. En sortie nous utiliseront le fichier vectors{_en}.txt.
- `../NaturalLanguageProcessing_ESGI_5IABD_S1/scraper/quick_termofuse_api.py` C'est le coeur du projet, l'API.

## Télécharger les fichiers
Se rendre sur l'url : https://drive.google.com/drive/folders/1uLF7agKs4j2i-DhUTdmLfYK0QEmkGEFi?usp=sharing puis télécharger les fichiers et les placer dans le dossier `../NaturalLanguageProcessing_ESGI_5IABD_S1/files/`.

Ne pas oublier de dézipé le fichier `corpus_cgu_folder.zip` si vous souhaité tester le script `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Aargan/check_important_word_in_sentences.py` et `../NaturalLanguageProcessing_ESGI_5IABD_S1/modele/Aargan/check_important_word_in_sentences_en.py`.
- `vectors.txt` Vecteur de mots en français dans 24 de corpus.
- `vector_2.txt` Vecteur de mots en français dans 1206 corpus. Attention un filtre est appliqué sur les sentences pour récupéré seulement celle en français. 
- `vector_en.txt` Vecteur de mots en français dans 1206 corpus. Attention un filtre est appliqué sur les sentences pour récupéré seulement celle en Anglais.
- `top_word.txt` Liste des mots ayants le plus d'occurence dans les phrase en français. 
- `top_word_en.txt` Liste des mots ayants le plus d'occurence dans les phrase en anglais.
- `corpus_cgu_folder.zip` Dossier contenant l'ensemble de nos corpus récupérer
- `CGU_FR.txt` Contient l'ensemble des corpus en français.
- `CGU_EN.txt` Contient l'ensemble des corpus en anglais.
