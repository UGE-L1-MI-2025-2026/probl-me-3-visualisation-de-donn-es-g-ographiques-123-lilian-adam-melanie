from affichage import afficher_carte_coloree, dessiner_legende, get_departement, largeur, hauteur, HEADER_INDEX_POP
from requirements import fltk as fltk
from time import time


fltk.cree_fenetre(largeur,hauteur, affiche_repere=True)
FILEPATH = "departements-20180101-shp/departements-20180101"
epoque = 0
headers = get_departement("headers")
afficher_carte_coloree(FILEPATH, headers[HEADER_INDEX_POP+epoque])
print("done")
dessiner_legende()

while True:
    fltk.mise_a_jour()
    event = fltk.donne_ev()
    type_event = fltk.type_ev(event)
    
    if type_event == "Quitte":
        break

    if type_event == "Touche" and event[1].char == "\r":
        epoque += 1
        if epoque == len(headers[HEADER_INDEX_POP-1:]):
            epoque = 0

        print(headers[HEADER_INDEX_POP + epoque])
        start = time()
        afficher_carte_coloree(FILEPATH, headers[HEADER_INDEX_POP + epoque])
        end = time()

        print(f"temps de chargement: {round(end - start, 2)}s")

fltk.ferme_fenetre()
