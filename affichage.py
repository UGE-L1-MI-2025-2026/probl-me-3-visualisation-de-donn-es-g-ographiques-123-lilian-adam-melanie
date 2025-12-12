from requirements import fltk as fltk
from calculs import *

largeur = 1200
hauteur = 900
HEADER_INDEX_POP = 5

#chemin_dep = 'departements-20180101-shp/departements-20180101.shp'
#chemin_pop = ''


def dessiner_legende(epoque: str = "p21_pop"):
    taille_x = 100
    taille_y = hauteur // len(PALETTE_COULEURS)
    ax=largeur - taille_x
    ay=taille_y
    bx=largeur
    by=(taille_y**2)

    headers = get_departement("headers")
    epoques = headers[HEADER_INDEX_POP:]
    for epoque in epoques:
        pop_min = get_population_min(epoque)
        pop_max = get_population_max(epoque)
    for i, couleur in enumerate(PALETTE_COULEURS):
        ax=largeur - taille_x
        ay=taille_y * max(0, i)
        bx=largeur
        by=(taille_y**2) * i

        moy = (pop_max-pop_min)//8
        pop_année = pop_min + moy*i
            
        fltk.texte(ax-140, ay, pop_année)
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

    pop_max = get_population_max(epoque)
    pop_min = get_population_min(epoque)

    count = 0
    for num_dep in departements_shp:
        #print(f"{num_dep = }")
        points = departements_shp[num_dep][1]
        #print("num_dep, points", num_dep, points)
        num_dep_save = num_dep

        for i in range(len(num_dep)):
            if num_dep[i] == "_":
                num_dep = num_dep[0:i]
                break

        if num_dep[0:2] == "69":
            num_dep = "69"

        dep_pop = int(get_departement(num_dep)[epoque])
        col_dep = get_couleur(dep_pop, pop_min, pop_max, PALETTE_COULEURS)
<<<<<<< HEAD
        #col_dep = "white"
        #print(col_dep)

        fltk.polygone(points, couleur = "black", remplissage = col_dep, epaisseur = 1)
    
    

fltk.cree_fenetre(largeur,hauteur, affiche_repere=True)
#afficher_carte_coloree("departements-20180101-shp/departements-20180101")
afficher_carte_coloree("departements-20180101/departements-20180101.shp")
print("done")
dessiner_legende()

while True:
    fltk.mise_a_jour()
    event = fltk.donne_ev()
    type_event = fltk.type_ev(event)
    if type_event == "Quitte":
        break

fltk.ferme_fenetre
=======
        #print(col_dep)

        fltk.polygone(points, couleur = "black", remplissage = col_dep, epaisseur = 1)
        count += 1

    print(f"departements affichés: {count}")
>>>>>>> f3f7bb6d71ebaa7d089edc1fed3cc609ff1d1ad3

#print(GLOBAL_DEPARTEMENTS)

