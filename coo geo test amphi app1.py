#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Mélanie
#
# Created:     01/12/2025
# Copyright:   (c) Mélanie 2025
# Licence:     <your licence>
#-------------------------------------------------------------------------------

def main():
    pass

if __name__ == '__main__':
    main()


from math import log, tan, pi, radians, degrees

def mercator(long, lat):
    x = long
    y = degrees(log(tan(radians(lat) / 2 + pi / 4)))
    return x, y


def calcule_parametres(x_min, y_min, x_max, y_max, x_orig, y_orig, W, H) -> a, B, C:
    # a: scale; B = décalage des abscisse, C = décalage des ordonnées

    a_abscisses =  W / (x_max - x_min)
    a_ordonnees = H / (y_max - y_min)
    a = min(a_abscisses, a_ordonnees)

    B = x_orig - a * x_min
    C = Y_orig + a * y_min

    return a, B, C

place_point = lambda x, y, a, B, C: a * x + B, a * y + C

def place_point(x, y, a, B, C):
    return a*x + B, y*a + C
