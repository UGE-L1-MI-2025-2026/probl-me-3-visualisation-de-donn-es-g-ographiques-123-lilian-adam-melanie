from requirements import fltk as fltk
from calculs import *

largeur = 900
hauteur = 750

#chemin_dep = 'departements-20180101-shp/departements-20180101.shp'
#chemin_pop = ''


def dessiner_légende():
    pass

def afficher_carte_coloree():

    #departements = charger_departements(chemin_dep)
    '''pop_max = max()'''
    '''pop_min= min()'''

    #bbox = bbox_globale(departements)
    fltk.cree_fenetre(largeur,hauteur)

    
    
    
    
    
    
    
    
    fltk.polygone([(2.3923284961351237, 48.335929161584076), (2.393003669902668, 48.336290983108846), (2.3940130169559044, 48.3356802622364), (2.3951130129955068, 48.3349251161054)],#points_dep, #points qui délimitent le département
    couleur='black',
    remplissage = 'blue', # pour plus tard : remp_coul variable change de couleurs en fonction des données
    epaisseur = 50
    )

#dessiner_legende()

afficher_carte_coloree()

while True:
    fltk.mise_a_jour()
    event = fltk.donne_ev()
    type_event = fltk.type_ev(event)
    if type_event == "Quitte":
        break

fltk.ferme_fenetre



