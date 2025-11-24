from fltk import *
import shapefile

def cree_fenetre(
        largeur: int, hauteur: int, frequence: int = 100,
        redimension: bool = False, affiche_repere : bool = False
) -> None:
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
        )
    __canevas = CustomCanvas(largeur, hauteur, frequence, resizing=redimension)
    if affiche_repere:
        repere()

@_fenetre_creee
def ferme_fenetre() -> None:
    """
    Détruit la fenêtre.
    """
    global __canevas
    assert __canevas is not None
    __canevas.root.destroy()
    __canevas = None
    __img_cache.clear()
    __img_stats.clear()

@_fenetre_creee
def mise_a_jour() -> None:
    """
    Met à jour la fenêtre. Les dessins ne sont affichés qu'après
    l'appel à cette fonction.
    """
    assert __canevas is not None
    __canevas.update()

@_fenetre_creee
def polygone(
        points: List[float],
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    assert __canevas is not None
    if epaisseur == 0:
        couleur = ""
    return __canevas.canvas.create_polygon(
        points, fill=remplissage, outline=couleur, width=epaisseur, tags=tag
    )


'''
sf = shapefile.Reader("departements-20180101") 
sf.records()
[...,
Record #47: ['77', 'Seine-et-Marne', 'FR102', 
             'fr:Seine-et-Marne', 5927.0],
...]
seine_et_marne = sf.shape(47) # Récupération de l'entrée correspondant à la Seine-et-Marne
seine_et_marne.bbox # Les points extrémaux de la seine-et-marne
[2.3923284961351237, 48.12014561527111, 
3.559220826259302, 49.11789167125887]
seine_et_marne.points # La liste des points du contour de la Seine-et-Marne
[(2.3923284961351237, 48.335929161584076), 
 (2.393003669902668, 48.336290983108846), 
 (2.3940130169559044, 48.3356802622364), ...]'''