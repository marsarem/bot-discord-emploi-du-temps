# Bot Discord de gestion d'emploi du temps
C'est un bot discord qui permet de gérer un emploi du temps facilement. Il a été créé pour avoir un emploi du temps des cours en visioconférence directement sur discord lors du confinement de la France en 2020 à cause du Covid-19.
Les auteurs sont .... et moi-même.

![Screenshot du bot](EDT_exemple_discord.png?raw=true "Screenshot du bot en fonctionnement dans discord")
![Screenshot du bot](EDT_exemple.png?raw=true "Fichier png d'un emploi du temps généré par le bot")

Si vous avez besoin d'aide pour le configurer, n'hésitez pas à me demander. Vous pouvez aussi me demander si vous voulez d'autres fonctionnalités en ouvrant une issue sur github.

Vous pouvez aussi me soutenir, voici mes addresses BTC et ETH:\
BTC : ....\
ETH : .... 


## Commandes :
Le prefix des commandes est configurable comme vous voulez dans le code (Par défaut : `!`)\
La commande `aide` permet d'afficher l'aide\
La commande `cours` permet d'afficher l'emploi du temps\
Les commandes `ajouter`, `supprimer` et `renommer` permettent de modifier l'emploi du temps.


## Pour lancer le bot :
Il faut remplacer "VOTRE TOKEN" par le token de votre bot dans le fichier bot.py (ligne 29)
Vous pouvez aussi changer le prefixe, c'est la ligne du dessous
Il faut ensuite lancer le bot avec python 3 (au moins python 3.6)


## Fonctionnement du bot :
Le bot fonctionne avec :\
- une base de donnée sqlite3 qui stocke tous les cours de tous les serveurs.\
- une image png de l'emploi du temps qui est crée à chaque changement de cours (quand on utilise la commande ajouter, supprimer ou renommer).

On peut utiliser ce bot sur autant de serveurs que l'on veut, les emplois du temps sont spécifique à chaque serveur. Pour utiliser le même emploi du temps dans plusieurs serveur, c'est possible mais il faut le définir dans le code.


## Modules nécessaires:
Les modules nécessaires sont les suivants (ils peuvent être installés avec pip):\
- discord (>= 1.0)\
- pillow