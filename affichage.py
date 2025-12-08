from requirements import fltk as fltk
from calculs import *

largeur = 1200
hauteur = 900

#chemin_dep = 'departements-20180101-shp/departements-20180101.shp'
#chemin_pop = ''


def dessiner_legende():
    taille_x = 100
    taille_y = hauteur // len(PALETTE_COULEURS)
    for i, couleur in enumerate(PALETTE_COULEURS):
        ax=largeur - taille_x
        ay=taille_y * max(1, i), 
        bx=largeur
        by=(taille_y**2) * i,
            
        fltk.texte(ax, ay, "oe")
        fltk.rectangle(
            ax, ay, bx, by,
            couleur = "black", remplissage=couleur, epaisseur=1
        )

def get_index_str_in_lst(lst, string) -> int:
    index = 0
    for s in lst:
        if s == string:
            return index
        index += 1

    return -1

def afficher_carte_coloree(file_name, epoque: str = "p21_pop"):
    departements_shp = get_mercator_from_shp(file_name, (largeur, hauteur))
    headers = get_departement("headers")

    pop_max = get_population_max(epoque)
    pop_min = get_population_min(epoque)

    for num_dep in departements_shp:
        points = departements_shp[num_dep][1]
        dep_pop = int(get_departement(num_dep)[epoque])
        col_dep = get_couleur(dep_pop, pop_min, pop_max, PALETTE_COULEURS)
        print(col_dep)

        fltk.polygone(points, couleur = "black", remplissage = col_dep, epaisseur = 1)
    
    
    
    fltk.polygone([(2.3923284961351237, 48.335929161584076), (2.393003669902668, 48.336290983108846), (2.3940130169559044, 48.3356802622364), (2.3951130129955068, 48.3349251161054)],#points_dep, #points qui délimitent le département
    couleur='black',
    remplissage = 'blue', # pour plus tard : remp_coul variable change de couleurs en fonction des données
    epaisseur = 5
    )

fltk.cree_fenetre(largeur,hauteur, affiche_repere=True)
afficher_carte_coloree("departements-20180101-shp/departements-20180101")
print("done")
dessiner_legende()

while True:
    fltk.mise_a_jour()
    event = fltk.donne_ev()
    type_event = fltk.type_ev(event)
    if type_event == "Quitte":
        break

fltk.ferme_fenetre



