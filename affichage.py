from fltk import *
@_fenetre_creee
def polygone(
        points: List[float],
        couleur: str = "black",
        remplissage: str = "",
        epaisseur: float = 1,
        tag: str = "",
) -> int:
    """
    Trace un polygone dont la liste de points est fournie.

    :param list points: liste de couples (abscisse, ordonnee) de points
    :param str couleur: couleur de trait (défaut 'black')
    :param str remplissage: couleur de fond (défaut transparent)
    :param float epaisseur: épaisseur de trait en pixels (défaut 1)
    :param str tag: étiquette d'objet (défaut : pas d'étiquette)
    :return: identificateur d'objet
    """
    assert __canevas is not None
    if epaisseur == 0:
        couleur = ""
    return __canevas.canvas.create_polygon(
        points, fill=remplissage, outline=couleur, width=epaisseur, tags=tag
    )

    
