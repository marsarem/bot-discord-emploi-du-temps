#---------------
import sqlite3
import discord
import sys
import os
import time
import json
import operator
import datetime
from asyncio import sleep as asleep
from random import shuffle
from PIL import Image, ImageDraw, ImageFont
#---------------


# discord v1.0


class Cours():
	def __init__(self):
		self.conn = sqlite3.connect('cours.db')

		self.creationBdd()
		# self.generer_nouvelle_image("401469621624111116")
		
		self.bot()

	def bot(self):
		TOKEN = "VOTRE TOKEN" # Mettre votre token

		PREFIX = "=" # Changer le préfix

		bot = discord.Client()
		
		@bot.event
		async def on_ready():
			jour = datetime.datetime.now().strftime("%d/%m/%Y à %H:%M:%S")
			print()
			print('------')
			print()
			print(f'Bot démarré le {jour}')
			print()
			print(bot.user.name)
			print(bot.user.id)
			print(f"Nb de users : {len(set(bot.get_all_members()))}")
			print('------')


		@bot.event
		async def on_message(message):
			serveur = message.guild.id
			
			# ICI vous pouvez rajouter une regle pour avoir le même emploi du temps pour différents serveur
			# Exemple :
			"""
			if message.guild.id == id_serveur_secondaire:
				serveur = str(id_serveur_principal)
			"""


			if message.author == bot.user:
				return

			if message.author.bot == True:
				return


			if message.content.startswith(f"{PREFIX}kill") and message.author.id == 257255974480510976:
				print("\n\n------------------------\nKilled\n------------------------\n\n")
				await bot.logout()
				return

			if message.content.startswith(f"{PREFIX}aide"):
				embed = discord.Embed(title="Aide :", color=0x00ff00)
				embed.add_field(name=f"{PREFIX}cours", value=f"Afficher le planning des cours (utilisable par tout le monde)", inline=False)
				embed.add_field(name=f"{PREFIX}ajouter", value=f"Ajouter un cours (uniquement pour les profs)", inline=False)
				embed.add_field(name=f"{PREFIX}enlever", value=f"Enlever un cours (uniquement pour les profs)", inline=False) 
				embed.add_field(name=f"{PREFIX}renommer", value=f"Renommer un cours (uniquement pour les profs)", inline=False) 
				embed.add_field(name=f"A Propos", value=f"Conçu par les meilleurs. (En python)")
				await message.channel.send(embed=embed)
				return

			if message.content.startswith(f"{PREFIX}cours"):
				cours = self.recupCours(serveur)
				#print(cours)
				try:
					file = discord.File(f"EDT_{serveur}.png")
				except Exception as e:
					await message.channel.send(f"Erreur, aucun emploi du temps détecté.\n(Voici l'erreur : {e})\n\nGénération d'un nouvel emploi du temps...")
					self.generer_nouvelle_image(serveur)
					file = discord.File(f"EDT_{serveur}.png")
					return
				finally:
					await message.channel.send(file=file)


			if message.content.startswith(f"{PREFIX}ajouter"):
				def check(m):
					return m.author == message.author and m.channel == message.channel

				await  message.channel.send(f"Ecrivez le nom du cours que vous voulez ajouter (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					nom = msg.content
				else:
					await  message.channel.send(f"Ajout annulé")
					return

				await  message.channel.send(f"Ecrivez le jour auquel vous voulez ajouter un cours (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					jour = msg.content.lower()
				else:
					await  message.channel.send(f"Ajout annulé")
					return

				await  message.channel.send(f"Ecrivez l'heure du début du cours à ajouter (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					if msg.content.lower() in ["lundi","mardi","mercredi","jeudi","vendredi"]:
						await  message.channel.send(f"Erreur, il faut écrire un jour de la semaine")
						return
					h_debut = msg.content.lower()
				else:
					await  message.channel.send(f"Ajout annulé")
					return

				await  message.channel.send(f"Ecrivez l'heure de fin du cours à ajouter  (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					h_fin = msg.content.lower()
				else:
					await  message.channel.send(f"Ajout annulé")
					return
			

				def heure(string):
					if "h" not in string.lower():
						string += "h"
					return string.lower()

				retour = self.ajouterUnCours(nom,jour,heure(h_debut),heure(h_fin),serveur)
				if retour[0] == "Error":
					await  message.channel.send("Erreur : "+retour[1])
				else:
					await message.channel.send("Le cours a bien été ajouté.")
					self.generer_nouvelle_image(serveur)
				return


			if message.content.startswith(f"{PREFIX}enlever") or message.content.startswith(f"{PREFIX}supprimer"):
				def check(m):
					return m.author == message.author and m.channel == message.channel

				await  message.channel.send(f"Ecrivez le jour auquel vous voulez enlever un cours (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					jour = msg.content.lower()
				else:
					await  message.channel.send(f"Suppression annulée")
					return

				await  message.channel.send(f"Ecrivez l'heure du début du cours à supprimer (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					if msg.content.lower() in ["lundi","mardi","mercredi","jeudi","vendredi"]:
						await  message.channel.send(f"Erreur, il faut écrire un jour de la semaine")
						return
					h_debut = msg.content.lower()
				else:
					await  message.channel.send(f"Suppression annulée")
					return

				await  message.channel.send(f"Ecrivez l'heure de fin du cours à supprimer (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					h_fin = msg.content.lower()
				else:
					await  message.channel.send(f"Suppression annulée")
					return


				def heure(string):
					if "h" not in string.lower():
						string += "h"
					return string.lower()

				retour = self.enleverUnCours(jour.lower(),heure(h_debut),heure(h_fin),serveur)
				if retour[0] == "Error":
					await  message.channel.send("Erreur : "+retour[1])
				else:
					await message.channel.send("Le cours a bien été enlevé.")
					self.generer_nouvelle_image(serveur)
				return



			if message.content.startswith(f"{PREFIX}renommer"):
				def check(m):
					return m.author == message.author and m.channel == message.channel

				await  message.channel.send(f"Ecrivez le jour auquel vous voulez renommer un cours (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					jour = msg.content.lower()
				else:
					await  message.channel.send(f"Renommage annulé")
					return

				await  message.channel.send(f"Ecrivez l'heure du début du cours à renommer (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					if msg.content.lower() in ["lundi","mardi","mercredi","jeudi","vendredi"]:
						await  message.channel.send(f"Erreur, il faut écrire un jour de la semaine")
						return
					h_debut = msg.content.lower()
				else:
					await  message.channel.send(f"Renommage annulé")
					return

				await  message.channel.send(f"Ecrivez l'heure de fin du cours à renommer (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					h_fin = msg.content.lower()
				else:
					await  message.channel.send(f"Renommage annulé")
					return

				await  message.channel.send(f"Ecrivez le nouveau nom pour le cours (Ecrivez annuler pour annuler): ")
				msg = await bot.wait_for('message', timeout=60.0, check=check)
				if msg.content.lower() != "annuler":
					nom = msg.content
				else:
					await  message.channel.send(f"Renommage annulé")
					return

				def heure(string):
					if "h" not in string.lower():
						string += "h"
					return string.lower()

				retour = self.enleverUnCours(jour.lower(),heure(h_debut),heure(h_fin),serveur)
				if retour[0] == "Error":
					await  message.channel.send("Erreur : "+retour[1])
				else:
					retour = self.ajouterUnCours(nom,jour.lower(),heure(h_debut),heure(h_fin),serveur)
					if retour[0] == "Error":
						await  message.channel.send("Erreur : "+retour[1])
					else:
						await message.channel.send("Le cours a bien été renommé.")
						self.generer_nouvelle_image(serveur)
				return

		bot.run(TOKEN)

	#---------------
	#Traitement de l'image
	#---------------
	def generer_nouvelle_image(self,serveur):
		#print("GENERATION")
		COURS = self.recupCours(serveur)

		liste_couleur = []
		for a in range (3):
			for b in range(3):
				for c in range(3):
					if not a == b == c:
						liste_couleur.append((75+70*a,75+70*b,75+70*c))

		liste_matiere = []
		for cle,valeur in COURS.items():
			if valeur == []:
				continue
			for i in valeur:
				if i[0] not in liste_matiere:
					liste_matiere.append(i[0])

		if "Physique Chimie" in liste_matiere:
			liste_couleur.remove((75,215,215))
		if "Espagnol" in liste_matiere:
			liste_couleur.remove((215,215,145))
		if "Maths" in liste_matiere:
			liste_couleur.remove((215,75,75))
		if "Anglais" in liste_matiere:
			liste_couleur.remove((75,145,215))
		if "SVT" in liste_matiere:
			liste_couleur.remove((145,215,75))

		shuffle(liste_couleur)

		associe_matiere_couleur = {}
		a = 0
		for i in liste_matiere:
			associe_matiere_couleur[i] = liste_couleur[a]
			a += 1

		associe_matiere_couleur["Physique Chimie"] = (75,215,215)
		associe_matiere_couleur["Espagnol"] = (215,215,145)
		associe_matiere_couleur["Histoire Géo"] = (21,115,11)
		associe_matiere_couleur["Maths"] = (215,75,75)
		associe_matiere_couleur["Anglais"] = (75,145,215)
		associe_matiere_couleur["SVT"] = (145,215,75)


		H, L, l = 400, 600, 530
		jours = ["LUNDI", "MARDI", "MERCREDI", "JEUDI", "VENDREDI"]
		arial = ImageFont.truetype("arial.ttf", 13)

		def mettreHeureEnForme(string):
			if 'h' not in string:
				return int(string)
			liste = string.lower().split("h")
			if liste[1] == "":
				return int(string.replace("h",""))
			return int(liste[1])/60+int(liste[0])

		im = Image.new("RGB", (l+10,H+20), "lightgrey")
		EDT = ImageDraw.Draw(im)

		for i in range(0, 12):
			EDT.line((L/6-70, H*i/11+10) + (l, H*i/11+10), fill="black")
		for i in range(0, 12):
			EDT.line((L/6-70, H/22+H*i/11+10) + (l, H/22+H*i/11+10), fill=(170, 170, 170))
		for i in range(1, 7):
			EDT.line((L*i/6-70, 10) + (L*i/6-70, H+10), fill="black")
		for i in range(1, 12):
			msg = str(i+7)+"h"
			w, v = arial.getsize(msg)
			EDT.text((L/6-w-3-70 , H*i/11+10-v/2), msg, font=arial, fill="black")
		for i in range(1,6):
			EDT.rectangle(((L*i/6+1-70, 10+1),(L*(i+1)/6-1-70, H/11+10-1)),fill=(150, 150, 150))
		for i in range(5):
			msg = jours[i]
			w, v = arial.getsize(msg)
			EDT.text((L*(2*i+3)/12 - w/2 -70, 10+H/22-v/2), msg, font=arial, fill="black")
			for cours in COURS[jours[i].lower()]:
				h1, h2 = mettreHeureEnForme(cours[1]), mettreHeureEnForme(cours[2])
				EDT.rectangle((((i+1)*L/6+1-70, (h1-7)*H/11+11),((i+2)*L/6-1-70, (h2-7)*H/11+9)), fill=associe_matiere_couleur[cours[0]])

				EDT.line(((i+1)*L/6+1-70, (h1-7)*H/11+10) + ((i+2)*L/6-1-70, (h1-7)*H/11+10), fill="black")#ligne à rajouter
				EDT.line(((i+1)*L/6+1-70, (h2-7)*H/11+10) + ((i+2)*L/6-1-70, (h2-7)*H/11+10), fill="black")#ligne à rajouter

				msg = cours[0]
				w, v = arial.getsize(msg)
				EDT.text((((i+2)*L/6-1-70 + (i+1)*L/6+1-70)/2 -w/2 , ((h1-7)*H/11+11 + (h2-7)*H/11+9)/2 - v/2), msg, font=arial, fill="black")

		im.save(f'EDT_{serveur}.png')
		return



	#---------------
	#Fonction autour de la bdd
	#---------------
	def creationBdd(self):
		cursor = self.conn.cursor()
		cursor.execute("""
		CREATE TABLE IF NOT EXISTS cours(
			id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
			matiere TEXT,
			jour TEXT,
			heure_debut TEXT,
			heure_fin TEXT,
			serveur TEXT
			)
			""")
		self.conn.commit()


	def recupCours(self, serveur):
		data = {}
		for jour in ["lundi","mardi","mercredi","jeudi","vendredi"]:
			data[jour] = []
			cursor = self.conn.cursor()
			cursor.execute("""SELECT id,matiere,heure_debut,heure_fin FROM cours WHERE jour = ? AND serveur = ?""",(jour,serveur))
			for row in cursor:
				data[jour].append([row[1],row[2],row[3]])

			data[jour] = sorted(data[jour], key=operator.itemgetter(2))
		return data


	def ajouterUnCours(self,matiere,jour,heure_debut,heure_fin,serveur):
		retour = self.chercherUnCours_add(jour,heure_debut,heure_fin,serveur)
		if retour[0] == "Trouve":
			return ["Error", f"Un cours est déjà présent le même jour et à la même heure : \nMatière : {retour[2]}\nJour : {retour[3]}\nHeure de début : {retour[4]}\nHeure de fin : {retour[5]}"]
		
		cursor = self.conn.cursor()
		cursor.execute("""
		INSERT INTO cours(matiere,jour,heure_debut,heure_fin,serveur) VALUES(?,?,?,?,?)""", (matiere,jour,heure_debut,heure_fin,serveur,))

		self.conn.commit()
		return ["Success"]


	def chercherUnCours_add(self,jour,heure_debut,heure_fin,serveur):
		def mettreHeureEnForme(string):
			string = str(string)
			if "." in string:
				return float(string)
			if 'h' not in string:
				return int(string)
			liste = string.lower().split("h")
			if liste[1] == "":
				return int(string.replace("h",""))
			return int(liste[1])/60+int(liste[0])


		cursor = self.conn.cursor()
		cursor.execute("""SELECT id,matiere,jour,heure_debut,heure_fin FROM cours WHERE jour = ? AND serveur=?""",(jour,serveur,))
		# requete dans BDD
		
		for row in cursor:
			#print(row,"---")
			data = ["Trouve", row[0], row[1], row[2], row[3], row[4]] 
			cours_a_enregistrer = []
			heure_debut = mettreHeureEnForme(heure_debut)
			heure_fin = mettreHeureEnForme(heure_fin)
			heure_debut_old = mettreHeureEnForme(row[3])
			heure_fin_old = mettreHeureEnForme(row[4])
			# print("-----------")
			# print(heure_debut,heure_fin)
			# print(heure_debut_old,heure_fin_old)
			# print(row[1])

			for i in range(int(float(heure_debut)*2)+1,int(float(heure_fin)*2)+1):
				cours_a_enregistrer.append(i)
			for i in range(int(float(heure_debut_old)*2)+1,int(float(heure_fin_old)*2)+1):
				if i in cours_a_enregistrer:
					# data[4] = mettreHeureEnForme(data[4])
					# data[5] = mettreHeureEnForme(data[5])
					return data

			#return ["PasTrouve"]
			
		return ["PasTrouve"]


	def enleverUnCours(self,jour,heure_debut,heure_fin,serveur):
		retour = self.chercherUnCours_remove(jour,heure_debut,heure_fin,serveur)
		if retour[0] == "PasTrouve":
			return ["Error","Aucun cours n'est prévu sur cet horaire."]
	
		cursor = self.conn.cursor()
		cursor.execute("""
		DELETE FROM cours WHERE id = ?""", (retour[1],))
		self.conn.commit()
		return ["Success"]


	def chercherUnCours_remove(self,jour,heure_debut,heure_fin,serveur):
		cursor = self.conn.cursor()
		cursor.execute("""SELECT id,matiere,jour,heure_debut,heure_fin FROM cours WHERE jour=? AND heure_debut=? AND heure_fin=? and serveur=?""",(jour,heure_debut,heure_fin,serveur,))
		
		for row in cursor:
			data = ["Trouve", row[0], row[1], row[2], row[3], row[4]]
			return data
			
		return ["PasTrouve"]

if __name__ == '__main__':
	cours = Cours()