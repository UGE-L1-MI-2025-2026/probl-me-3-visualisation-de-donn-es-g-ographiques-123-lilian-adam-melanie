from requirements import fltk as fltk
from calculs import *

largeur = 1200
hauteur = 900

#chemin_dep = 'departements-20180101-shp/departements-20180101.shp'
#chemin_pop = ''


def dessiner_legende():
    xo = largeur - 40
    yo = 20
    ho = hauteur - 40
    fltk.rectangle(ax=xo, ay=yo, bx=xo+ho, by=yo+ho, couleur = 'black', remplissage='red', epaisseur=5)

def afficher_carte_coloree(file_name):

    #departements = charger_departements(chemin_dep)
    departments = get_mercator_from_shp(file_name, 0.00005)
    '''pop_max = max()'''
    '''pop_min= min()'''

    #bbox = bbox_globale(departements)
    fltk.cree_fenetre(largeur,hauteur)

    for department in departments:
        points = departments[department][1]
        #print(points)

        fltk.polygone(points, couleur = "black", remplissage = "blue", epaisseur = 1)
    
    
    
    
    
    
    
    fltk.polygone([(2.3923284961351237, 48.335929161584076), (2.393003669902668, 48.336290983108846), (2.3940130169559044, 48.3356802622364), (2.3951130129955068, 48.3349251161054)],#points_dep, #points qui délimitent le département
    couleur='black',
    remplissage = 'blue', # pour plus tard : remp_coul variable change de couleurs en fonction des données
    epaisseur = 5
    )

#dessiner_legende()

afficher_carte_coloree("departements-20180101-shp.zip/departements-20180101.shp")
print("done")
dessiner_legende()

while True:
    fltk.mise_a_jour()
    event = fltk.donne_ev()
    type_event = fltk.type_ev(event)
    if type_event == "Quitte":
        break

fltk.ferme_fenetre



