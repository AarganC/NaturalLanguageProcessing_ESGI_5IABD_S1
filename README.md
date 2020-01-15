# NaturalLanguageProcessing_ESGI_5IABD_S1

## Utiliser l'environnement conda du Plugin/API
- Aller à la racine du projet
- Lancer la commande `conda env create -f conda_env/env_nlp.yaml`
- Lancer la commande `conda activate env_nlp`

## Test du Plugin/API
- Ouvrir un terminal
- Activer l'environnement `conda activate env_nlp`
- Aller à la racine du projet
- Lancer la commande `python quick_termofuse_api.py`
- Ouvrir l'application `google chrome`
- Dans l'url écrire `chrome://extensions/`
- Activer `Developer mode` (en haut a droite dans mon cas)
- Ensuite vous devriez avoir le bouton `Load unpacked` qui apparait
- Selectionner le dossier `plugin_chrome`
- Puis aller sur un la parti CGU ou cookie d'un site (example : http://mentions-legales.lefigaro.fr/page/cgu)
- cliquer sur le bouton `Check this website now!`

Pour le moment le plugin/API fonctionne seulement en local, il faut 2 semaines de validation pour pouvoir en publier un.
