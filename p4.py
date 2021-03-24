import numpy as np
import matplotlib.pyplot as plt
import random 
import os

plateau = np.zeros((7,7))

H = 4

def choix_colonne():
	colonne = 0
	
	while (colonne > 7) or (colonne < 1) :
		try :
			colonne = int(input("[J" + str(k%2+1) + "] Choisissez la colonne : "))
			
			if plateau[6,colonne-1] != 0:
				print('Colonne déjà pleine')
				colonne = 0
				
		except ValueError:
			print ('Rentrer un entier')
			colonne = 0
	
	return colonne - 1

def placement_pion(plateau,colonne):
	case_vide = 0  
	
	try:
		while plateau[case_vide, colonne] != 0 :
			case_vide += 1
		return case_vide
	
	except IndexError:
		return case_vide

def check_victoire(plateau):
	victoire = False
	
	for i in range(7):
		for j in range(7):
		
			try:
				A = (plateau[i,j] == plateau[i,j+1] == plateau[i,j+2] == plateau[i,j+3])
				B = (plateau[i,j] == plateau[i+1,j] == plateau[i+2,j] == plateau[i+3,j])
				C = (plateau[i,j] == plateau[i+1,j+1] == plateau[i+2,j+2] == plateau[i+3,j+3])
				D = (plateau[i,j] == plateau[i-1,j+1] == plateau[i-2,j+2] == plateau[i-3,j+3]) 
			except IndexError:
				A,B,C,D = False,False,False,False
				
			if (A or B or C or D) and plateau[i,j] != 0:
				victoire = True
				return victoire
			
	return victoire
	
def plot_grille(plateau,k):
	
	plt.axis('off')
	
	if k%2 + 1 == 1:
		Color = 'yellow'
	else:
		Color = 'red'
	
	for i in range(8):
		plt.plot([i,i], [0,7], color = 'black', linewidth = 2)
		
	for i in range(7):
		plt.plot([0,7], [i,i], color = 'black', linewidth = 2)
		
	plt.scatter(8, 3, s = 800, marker = '8', color = Color, edgecolors = 'black', linewidths = 1)
		
	for i in range(7):
		for j in range(7):
			
			if plateau[i,j] == 1:
				plt.scatter(j + 0.5, i + 0.5, s = 800, marker = '8', color = 'yellow', edgecolors = 'black', linewidths = 1)
			elif plateau[i,j] == 2:
				plt.scatter(j + 0.5, i + 0.5, s = 800, marker = '8', color = 'red', edgecolors = 'black', linewidths = 1)	
				
def check_victoire_ordi(T):
	victoire = False	
	
	for i in range(7):
		for j in range(7):
		
			try:
				A = (T[i,j] == T[i,j+1] == T[i,j+2] == T[i,j+3])
				B = (T[i,j] == T[i+1,j] == T[i+2,j] == T[i+3,j])
				C = (T[i,j] == T[i+1,j+1] == T[i+2,j+2] == T[i+3,j+3])
				D = (T[i,j] == T[i-1,j+1] == T[i-2,j+2] == T[i-3,j+3]) 
			except IndexError:
				A,B,C,D = False,False,False,False
				
			if (A or B or C or D) and T[i,j] != 0:
			
				victoire = True
				return victoire, T[i,j]
			
	return victoire, 0
				
def evaluation(T):

	note = 0
	
	if (check_victoire_ordi(T)[0] == True) and (check_victoire_ordi(T)[1] == 1):
		note -= 100
	elif (check_victoire_ordi(T)[0] == True) and (check_victoire_ordi(T)[1] == 2):
		note += 100
	
	return note
	
def Note(T,h):
	note = [0]*7
	
	if h < H:
		for j in range(7):
			plateau_prime = np.copy(T)
			
			if h%2 == 1:
				try:
					plateau_prime[placement_pion(plateau_prime,j),j] = 2
					note[j] = Note(plateau_prime,h+1)
				except IndexError:
					pass
			else:
				try:
					plateau_prime[placement_pion(plateau_prime,j),j] = 1
					note[j] = Note(plateau_prime,h+1)
				except IndexError:
					pass
			
		if h%2 == 1:
			return max(note)
		else:
			return min(note)
			
	else:
		return evaluation(T)

def jeu(plateau):
	note = [0]*7
	
	for x in range(7):
		plateau_prime = np.copy(plateau)
		try:
			plateau_prime[placement_pion(plateau_prime,x),x] = 2
		except IndexError:
			pass
		note[x] = Note(plateau_prime,0)
	print(note)
	if note.count(0) == 7:
		print("random")
		return random.randint(0,6)
	else:
		print("pas random")
		return note.index(max(note))
					
			


k = -1 #permet de savoir quel joueur est entrain de jouer
mode = 0
while (mode != 1) and (mode != 2):

	try:
		mode = int(input("Quelle mode ? \n[1]: Joueur contre joueur \n[2]: Joueur contre ordinateur\n"))
		if (mode != 1) and (mode != 2):
			print('Soit 1 ou 2 !')
			mode = 0
	except ValueError:
		mode = 0
		print('Rentrez un entier')
	
	
while (check_victoire(plateau) == False):
	k += 1
	# print (plateau)
	
	plot_grille(plateau,k)
	plt.pause(0.1)
		
		
	if k%2 == 0:	
		colonne = choix_colonne()
		plateau[placement_pion(plateau,colonne),colonne] = k%2 + 1
		if check_victoire(plateau) == True:
			break
		
	else:
		if mode == 2:
			os.system('cls')
			print("L'ordinateur réfléchi ...")
			colonne = jeu(plateau)
		else:
			os.system('cls')	
			colonne = choix_colonne()	
		plateau[placement_pion(plateau,colonne),colonne] = k%2 + 1
		if check_victoire(plateau) == True:
			break
		
		
		
plot_grille(plateau,k)
plt.pause(0.1)
			
print(plateau)
print("Le joueur " + str(k%2 + 1) + " a gagné")
os.system("pause")