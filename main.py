from affichage import afficher_carte_coloree
from requirements import fltk as fltk

if __name__ == "__main__":
    afficher_carte_coloree()

    while True:
        fltk.mise_a_jour()
        event = fltk.donne_ev()
        type_event = fltk.type_ev(event)
        if type_event == "Quitte":
            break

    fltk.ferme_fenetre