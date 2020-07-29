# FontCreator

Cet outil permet la création de police d'écriture pour les afficheurs de l'Hôtel Pasteur. Il est possible de choisir les LED à allumer en fonction de chacune des lettres puis de générer le code associé. Les fonctions d'import / export permettent de sauvegarde et d'échanger les fichiers de police.

## Installation

Ce logiciel nécessite python 3 et la librairie tkinter pour fonctionner et se lance depuis le fichier main. Si vous souhaitez créer un exécutable pour votre plateforme, il vous suffira d'installer pyinstaller et de lancer la commande make :

```bash
pip install --user pyinstaller # installation de pyinstaller
make # compilation du logiciel et de ses dependances
```

## License
[GPLv3](https://choosealicense.com/licenses/gpl-3.0/)