#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
What does this script:

This script replicates an experiment where the participant, after an initial training part has to rate the speeds of different objects
approaching towards him or her, on a seven-points Likert scale.
After the experiment itself, the participant has to complete a questionnaire about his or her fear of spiders.

How to run the program:

- Clone the github repository (https://github.com/Jeremie-Beucler/PCBS_spider_bias) on your computer using a terminal
- Launch the program from your terminal: it takes two argument (the objects you want to compare)

N.B.: the arguments must be names of .png pictures of the github repository.

E.g. if you want to compare the evaluation of the speed of a spider and of the speed of a fly, type: "python Spider_bias.py tegenaria_domestica.png musca_domestica.png"

All the data are stored in a .xpd file in the folder Data.
"""

import expyriment
import random
import sys
from statistics import mean

exp = expyriment.design.Experiment(name="Spider_bias")

expyriment.control.set_develop_mode(on=True)

expyriment.control.initialize(exp)

consignes_entraînement = expyriment.stimuli.TextScreen("Entraînement", "\nVous allez voir un cercle se déplacer à deux vitesses: vitesse 1 (la plus lente) et vitesse 7 (la plus rapide).\n(Appuyez sur une touche pour continuer)", heading_underline=True)
consignes_test = expyriment.stimuli.TextScreen("Expérience", "\nMaintenant que vous êtes familiarisés avec les deux vitesses extrêmes, indiquez pour chaque objet, sur une échelle allant de 1 (la plus lente) à 7 (la plus rapide), à quelle vitesse il s'est déplaçé. \n\n(Appuyez sur une touche pour continuer)", heading_underline=True)
consignes_questionnaire = expyriment.stimuli.TextScreen("Questionnaire", "\nMerci d\'avoir participé à cette expérience. Avant de finir, veuillez compléter le questionnaire suivant. \n Choisissez une réponse sur l\'échelle de \"pas du tout d\'accord\" à \"tout à fait d\'accord\" pour chacun des 18 items.\n\n(Appuyez sur une touche pour continuer)", heading_underline=True)


def calc_pos(ancient_pos, verti_move, limit_verti):
	"""Defines the new position of a stimulus, whith a random horizontal movement and a fixed vertical one. 
	   When the stimulus crosses a fixed point on the y axis, the object makes a diagonal depending on which side
	   of the screen it was on the x axis.
	
	Args
	- ancient_pos(tuple): the previous position of the stimulus on the x and y axis
	- verti_move (int): the nb of pixel for the verti movement (i.e. the speed of the stimulus)
	- limit_verti (int): limit on the y axis for the stimulus to choose a side (left or right)
	
	Returns: the new position of the stimulus (tuple) and the degree of the rotation to apply to the stimulus (int)"""
		
	new_pos = [ancient_pos[0],(ancient_pos[1] + -1 * verti_move)]
	# translation du stimulus sur l'axe des y
	random_hori_move = random.randrange(-5,6,5)
	
	if new_pos[1] >= limit_verti:
		# si le stimulus n'a pas dépassé la limite sur l'axe des y
		degree_rotation = random_hori_move
		new_pos[0] += random_hori_move
	else: 
		if new_pos[0] >= 0:
		# si le stimulus était dans la partie droite de l'écran
			new_pos[0] += 5 * (verti_move//5)
			#le stimulus part à droite
			degree_rotation = 7 + (verti_move//5)
		else:
		# si le stimulus était dans la partie gauche de l'écran
			new_pos[0] += -1 * (5 * (verti_move//5))
			#le stimulus part à gauche
			degree_rotation = -7 - (verti_move//5)
		
	return new_pos, degree_rotation

question_test = ["A quelle vitesse s'est déplacé l'objet, sur une échelle allant de 1 à 7?"]
list_legendes_vitesse = []
for nb in range(1, 8):
	list_legendes_vitesse.append(str(nb))
	
def Likert_scale(N, legendes, questions):
	"""Draws a Likert scale with buttons and text for legend and questions
	
	Args:
		- N (int): nombre de points sur l'échelle (doit être impair: 5, 7, etc.)
		- legendes (list of strings): légendes à rajouter pour chaque case (ex: un peu d'accord, d'accord...)
		=> N et legendes permettent de créer l'échelle
		- questions (list of strings): liste de questions à poser au participant 
		=> questions permet de créer le questionnaire
	Returns: chaque question rentrée avec l'échelle correspondante (list of canvas), les positions des boutons de réponses (list of tuples)
			 le rayon des boutons de réponse (int), la position du bouton submit (tuple)
	"""
	
	extremite_echelle = int((N - 1)/2)
	#e.g. si l'échelle est à 7 points, on obtient 3 (l'échelle va de -3 à 3)
	distance_cercles = 700/N
	#on divise une partie de la toile (qui fait 800*600 pixels, voir + bas) par le nombre de points de l'échelle
	list_pos = []
	for i in range(-extremite_echelle, extremite_echelle + 1):
			list_pos.append(int(i * distance_cercles))
			#on calcule, sur l'axe horizontal, les positions des boutons de réponse
	
	list_button = []
	radius_button = 15
	list_text_leg = []
	for i in range(N):
			button = expyriment.stimuli.Circle(radius=radius_button, position=(list_pos[i],-50), colour=(0,0,0), line_width=2)
			list_button.append(button)
			text_leg = expyriment.stimuli.TextBox(legendes[i], position=(list_pos[i],0), size=(100, 50))
			list_text_leg.append(text_leg)
			#création des boutons de réponse avec leurs légendes
	
	list_can = []
	pos_submit_button = (225, -130)
	
	for i in range(len(questions)):
		toile = expyriment.stimuli.Canvas(size=(800,600), colour=(255,255,255))
		for elt in list_button:
			elt.plot(toile)
		for elt in list_text_leg:
			elt.plot(toile)
		text_question = expyriment.stimuli.TextBox(questions[i], position=(0,100), size=(700, 50), text_colour=(0,0,0))
		text_question.plot(toile)
		ok = expyriment.stimuli.Picture('ok.png', position=(pos_submit_button))
		ok.plot(toile)
		list_can.append(toile)
		#ajout pour chaque question d'une toile, et sur chaque toile de l'échelle, de la question, et d'un bouton pour valider ('ok.png')
		
	return(list_can, list_pos, radius_button, pos_submit_button)

question_file = open('questionnaire.txt')
lignes = question_file.readlines()
list_question = []
for elt in lignes:
	list_question.append(elt)
question_file.close()
#ajout de chaque question du questionnaire sur la peur des araignées dans une liste

list_legendes_points = ["Pas du tout\nd'accord", "Pas d'accord", "Plutôt pas\n d'accord", "D'accord", "Plutôt\nd'accord", "D'accord", "Tout à fait\nd'accord"]
				
exp.data_variable_names = ["Object type", "Real speed", "Perceived speed"]

expyriment.control.start()

consignes_entraînement.present()
exp.keyboard.wait()
speeds_training = [10, 70]
# les sujets ne voient pendant l'entraînement que les deux vitesses extrêmes
for i in range(0, 2):
	for speed in speeds_training:
		speed_to_display = "Vitesse " + str(speed//10)
		text_speed = expyriment.stimuli.TextScreen(speed_to_display, "\nObservez attentivement le cercle se déplacer à la "+ speed_to_display + "\n\n(Appuyez sur une touche pour continuer)")
		text_speed.present()
		exp.keyboard.wait()
		pos_circle = [0,400]
		while pos_circle[1] >= -350:
			pos_circle, deg_rot = calc_pos(pos_circle,speed,-75)
			toile_pieds = expyriment.stimuli.Canvas(size=(1000,800), colour=(255,255,255))
			sol = expyriment.stimuli.Picture('plancher.png')
			sol.plot(toile_pieds)
			feet_pic = expyriment.stimuli.Picture('feet.png', position=(0, -245))
			feet_pic.plot(toile_pieds)
			dot = expyriment.stimuli.Circle(radius=25, colour=(255, 0, 0), position=pos_circle)
			dot.plot(toile_pieds)
			toile_pieds.present()
			exp.clock.wait(1)
			#fait bouger le cercle pour chacune des deux vitesses, deux fois
	

consignes_test.present()
exp.keyboard.wait()

for object in range(1, len(sys.argv)):
	speeds = [10, 20, 30, 40, 50, 60, 70] * 2
	random.shuffle(speeds)
	#pour chaque objet, les participants voient toutes les vitesses deux fois dans un ordre aléatoire
			
	for speed in speeds:
		questionnaire, position_cercles, rad_button, pos_sub = Likert_scale(7, list_legendes_vitesse, question_test)
		#création de toutes les questions avec l'échelle en 7 points à chaque fois
		pos_pic = [0,400]
		while pos_pic[1] >= -350:
			pos_pic, deg_rot = calc_pos(pos_pic,speed,-75)
			toile_pieds = expyriment.stimuli.Canvas(size=(1000,800), colour=(255,255,255))
			sol = expyriment.stimuli.Picture('plancher.png')
			sol.plot(toile_pieds)
			feet_pic = expyriment.stimuli.Picture('feet.png', position=(0, -245))
			feet_pic.plot(toile_pieds)
			pic_stim = expyriment.stimuli.Picture(sys.argv[object], position=pos_pic)
			pic_stim.rotate(deg_rot)
			pic_stim.plot(toile_pieds)
			toile_pieds.present()
			exp.clock.wait(1)
			
		toile = questionnaire[0]
		toile.present()
		expyriment.io.Mouse(show_cursor=True)
		has_clicked_button = 0
		has_clicked_submit = 0
		while has_clicked_submit == 0:
			pos = exp.mouse.wait_press()
			pos_tuple = pos[1]
			#enregistre la position cliquée par le participant
			if has_clicked_button == 0:
			#si le participant clique pour la première fois dans un des boutons
				for elt in position_cercles:
					if pos_tuple[0] < elt + rad_button and pos_tuple[0] > elt - rad_button:
						if pos_tuple[1] < -50 + rad_button and pos_tuple[1] > -50 - rad_button:
						#si le participant a cliqué sur un des boutons
							circle_first_rep = expyriment.stimuli.Circle(radius=5, position=(elt, -50), colour=(0, 0, 255))
							circle_first_rep.plot(toile)
							#remplit le bouton cliqué d'un cercle bleu
							ancient_pos_clicked = (elt, -50)
							has_clicked_button += 1
							toile.present()
	
			elif has_clicked_button != 0:
			#si le participant a déjà répondu une fois
				for elt in position_cercles:
					if pos_tuple[0] < elt + rad_button and pos_tuple[0] > elt - rad_button:
						if pos_tuple[1] < -50 + rad_button and pos_tuple[1] > -50 - rad_button:
							circle_to_del = expyriment.stimuli.Circle(radius=rad_button, position=(ancient_pos_clicked), colour=(255,255,255), line_width=0)
							circle_to_del.plot(toile)
							ancient_circle = expyriment.stimuli.Circle(radius=rad_button, position=(ancient_pos_clicked), colour=(0,0,0), line_width=2)
							ancient_circle.plot(toile)
							#restaure l'ancien bouton cliqué à son état initial
							circle_has_rep = expyriment.stimuli.Circle(radius=5, position=(elt, -50), colour=(0, 0, 255))
							circle_has_rep.plot(toile)
							#remplit le nouveau bouton cliqué d'un cercle bleu
							toile.present()
							ancient_pos_clicked = (elt, -50)
		
				if pos_tuple[0] < (pos_sub[0] + rad_button) and pos_tuple[0] > (pos_sub[0] - rad_button):
					if pos_tuple[1] < (pos_sub[1] + rad_button) and pos_tuple[1] > (pos_sub[1] - rad_button):
						has_clicked_submit += 1
						#si le sujet clique sur le bouton valider, on passe à la question suivant
						score = (int(ancient_pos_clicked[0]/100 + 4))
						#permet de passer des positions des cercles (-300, -200, etc.) aux points (de 1 à 7 ici)
		
		exp.data.add([sys.argv[object], (speed //10), score])
	
consignes_questionnaire.present()
exp.keyboard.wait()

questionnaire, position_cercles, rad_button, pos_sub = Likert_scale(7, list_legendes_points, list_question)
#création de toutes les questions avec l'échelle en 7 points à chaque fois
list_score_quest = []
for toile in questionnaire:
	expyriment.io.Mouse(show_cursor=True)
	
	has_clicked_button = 0
	has_clicked_submit = 0
	
	while has_clicked_submit == 0:
#même code que précédemment
		toile.present()
		pos = exp.mouse.wait_press()
		pos_tuple = pos[1]
		#enregistre la position cliquée par le participant
		if has_clicked_button == 0:
		#si le participant clique pour la première fois dans un des boutons
			for elt in position_cercles:
				if pos_tuple[0] < elt + rad_button and pos_tuple[0] > elt - rad_button:
					if pos_tuple[1] < -50 + rad_button and pos_tuple[1] > -50 - rad_button:
					#si le participant a cliqué sur un bouton
						circle_first_rep = expyriment.stimuli.Circle(radius=5, position=(elt, -50), colour=(0, 0, 255))
						circle_first_rep.plot(toile)
						ancient_pos_clicked = (elt, -50)
						has_clicked_button += 1
	
		elif has_clicked_button != 0:
		#si le participant a déjà répondu une fois
			for elt in position_cercles:
				if pos_tuple[0] < elt + rad_button and pos_tuple[0] > elt - rad_button:
					if pos_tuple[1] < -50 + rad_button and pos_tuple[1] > -50 - rad_button:
						circle_to_del = expyriment.stimuli.Circle(radius=rad_button, position=(ancient_pos_clicked), colour=(255,255,255), line_width=0)
						circle_to_del.plot(toile)
						ancient_circle = expyriment.stimuli.Circle(radius=rad_button, position=(ancient_pos_clicked), colour=(0,0,0), line_width=2)
						ancient_circle.plot(toile)
						circle_has_rep = expyriment.stimuli.Circle(radius=5, position=(elt, -50), colour=(0, 0, 255))
						circle_has_rep.plot(toile)
						toile.present()
						ancient_pos_clicked = (elt, -50)
			
			if pos_tuple[0] < (pos_sub[0] + rad_button) and pos_tuple[0] > (pos_sub[0] - rad_button):
				if pos_tuple[1] < (pos_sub[1] + rad_button) and pos_tuple[1] > (pos_sub[1] - rad_button):
					has_clicked_submit += 1
					#si le sujet clique sur le bouton valider, on passe à la question suivant
					score = (int(ancient_pos_clicked[0]/100 + 4))
					#permet de passer des positions des cercles (-300, -200, etc.) aux points (de 1 à 7 ici)
		
	list_score_quest.append(score)
	
score_quest = sum(list_score_quest)
exp.data.add(["Score questionnaire", score_quest])

expyriment.control.end()
