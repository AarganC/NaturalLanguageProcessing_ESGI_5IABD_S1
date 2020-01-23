
Pour former nos propres vecteurs GloVe, nous devons d'abord préparer notre corpus de données CGU en tant que fichier texte unique avec tous les mots séparés par un ou plusieurs espaces ou tabulations. Une fois que notre corpus crée, on a reussi à former des vecteurs GloVe en utilisant les 4 outils suivants. Un exemple est inclus dans demo2.sh, qu'on peut  modifier si nécessaire.

Les quatre principaux outils de ce package sont:

1) vocab_count
Cet outil nécessite un corpus d'entrée qui devrait déjà être composé de jetons séparés par des espaces. Utilisez d'abord quelque chose comme le Tokenizer Stanford sur du texte brut. À partir du corpus, il construit des décomptes unigrammes à partir d'un corpus, et définit éventuellement le vocabulaire résultant en fonction de la taille totale du vocabulaire ou du décompte de fréquences minimum.

2) cooccur
Construit des statistiques de cooccurrence mot-mot à partir d'un corpus. L'utilisateur doit fournir un fichier de vocabulaire, tel que produit par vocab_count, et peut spécifier une variété de paramètres, comme décrit en exécutant ./build/cooccur.

3) shuffle
Mélange le fichier binaire des statistiques de cooccurrence produites par cooccur. Pour les fichiers volumineux, le fichier est automatiquement divisé en morceaux, chacun étant mélangé et stocké sur le disque avant d'être fusionné et mélangé ensemble. L'utilisateur peut spécifier un certain nombre de paramètres, comme décrit en exécutant ./build/shuffle.

4) glove
Entraînez le modèle GloVe sur les données de cooccurrence spécifiées, qui seront généralement la sortie du shuffle. L'utilisateur doit fournir un fichier de vocabulaire, comme indiqué par vocab_count, et peut spécifier un certain nombre d'autres paramètres, qui sont décrits en exécutant ./build/glove.
