# Générateur de gifs animés rigodrôles

## Introduction

Ce dépôt de code contient un script Python permettant la génération automatique d'images animées, en superposant plusieurs couches. Le script superpose une image animée en fond, divers éléments qui vont tournoyer au second plan, et enfin une image au premier plan.

Le nombre de trames de l'image générée est un multiple du nombre de trames de l'image de fond utilisée. Par exemple, si l'image de fond utilisée contient 16 trames, il est possible de générer une image animée avec 16, 32, 48, etc. trames.

Le nombre de rotations effectuées par les images au second plan est un nombre entier. Par exemple, certaines images pourront effectuer 3 rotations pendant que d'autres en effectueront une seule sur la durée totale de l'animation.

La taille de l'image finale générée est celle de l'image à utiliser au premier plan. Cela veut dire que l'image de l'arrière plan est redimensionnée dans cette même taille, ce qui peut l'étirer dans une direction si les deux n'ont pas le même ratio.

## Installation

Python 3 est requis. Les packages nécessaires peuvent être installés à l'aide de la commande suivante.
```
$ python -m pip install -r requirements.txt
```

## Utilisation

Pour exécuter le script, simplement utiliser la commande suivante.
```
$ python generate.py
```

Pour paramétrer l'image à générer, voici les différents éléments à modifier dans le script.
```python
background_image_name   = "background/bg4.gif"
frame_count_multiplier  = 1
frame_duration          = 0.04
photo_name              = "photo.png"
item_names              = [ "items/star.png",
                            "items/unicorn.png" ]
```

La chaîne `background_image_name` indique le nom du fichier qui servira d'image animée de fond. C'est un fichier au format GIF. La chaîne `photo_name` indique le nom du fichier qui servira d'image de premier plan. Cette image doit naturellement contenir des zones transparentes. Enfin, le tableau `item_names` indique les noms des fichiers des éléments à ajouter au second plan.

L'entier `frame_count_multiplier` sert à augmenter de nombre de frames de l'image animée produite. Il multiplie simplement la durée de l'image animée de fond par un facteur. Le nombre `frame_duration` indique la durée d'apparition de chaque frame, en seconde, dans l'image animée produite.

Enfin, le seul autre élément pertinent à modifier est le tableau qui décrit comment ajouter les éléments du second plan.
```python
item_data               = [ { "item_index": 0,
                              "size": (80, 80),
                              "position": (260, 200), 
                              "initial_angle": 120,
                              "rotation_speed": 1,
                              "rotation_direction": 1 } ]
```
Le champ `item_index` détermine quelle image du tableau `item_names` doit être utilisée. Le champ `size` détermnie la taille de l'image à appliquer (en pixels). Pour rappel, la taille totale de l'image est celle de la photo au premier plan. Le champ `position` détermine la position où placer l'élément sur l'image. Plus précisément, c'est le coin supérieur gauche de l'élément qui est placé à cette position. Le champ `initial_angle` permet de débuter la rotation avec un angle donné. Le champ `rotation_speed` permet d'augmenter la vitesse de rotation, pour réaliser plusieur tours durant le cycle de l'animation. Enfin, le champ `rotation_direction` peut prendre la valeur 1 ou -1 pour changer la direction de la rotation.
