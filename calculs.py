from requirements import shapefile as shapefile
import typing
from typing import List, Any
from pyexcel import get_sheet, Sheet
import json
import math

#import shapefile

def wgs_to_mercator(pos, map_scale) -> typing.Tuple[float, float]:
    R : float = 6378137.000
    lat, lon = pos[0], pos[1]

    x = R * math.radians(lon)
    scale = x / lon
    pi = math.pi
    y = 180 / pi * math.log(math.tan(pi/4.0 + lat * (pi/180.0)/2.0)) * scale

    x, y = x * map_scale, y * map_scale

    return (x, y)


def mercator_to_wgs():
    pass


def convert_wgs_to_mercator(departments, map_scale):
    departments_mercator : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = { 

    }

    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for point in departments[department][1]:
            new_point = wgs_to_mercator(point, map_scale)
            new_points.append(new_point)
        departments_mercator[department] = [ departments[department][0], new_points ]

    return departments_mercator


def import_csv(file_name):
    # csv
    pass


def import_netcdf(file_name):
    # module netCDF4
    pass


# -------------------------------SHAPEFILE----------------------------------------


def import_shp(file_name) -> shapefile:
    """
    Parameter: 
        file_name : str = name/path of the shapefile (.shp)
    Returns:
        sf : shapefile = the content of the shapefile file
    Imports a shp file and returns its content
    
    """
    # shapefile
    sf : shapefile = shapefile.Reader(file_name)

    return sf

def get_points(sf) -> typing.Dict[str, int]:
    """
    Parameter:
        sf : shapefile = content of a shapefile file
    Returns:
        departments : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[int, int]]]] = dictionnary where:
            keys : str = are the departments' ID
            values : list with list[0] being the name (str) and list[1] being the list of tuples = are the points making the outline of each department
    Take the IDs and list of points from the content of the shapefile and returns a dictionnary with the departments' ID and their outlines
    """

    departments : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[int, int]]]] = {

    }
    sf_shapes = sf.shapes()

    for i in range(len(sf_shapes)):
        curr_record = sf.record(i)
        departments[curr_record[0]] = [curr_record[1], sf.shape(i).points]
    return departments


def get_mercator_from_shp(file_name, map_scale):
    sf = import_shp(file_name)
    points = get_points(sf)
    mercator_points = convert_wgs_to_mercator(points, map_scale)
    return mercator_points
    

# sf = shapefile.Reader("departements-20180101-shp.zip/departements-20180101.shp")
# print(sf.records())
# print(sf.shape(0))
# print(sf.record(0)[0])
# print(get_points(sf)["30"])

# sf = import_shp("departements-20180101-shp.zip/departements-20180101.shp")
# points = get_points(sf)
# #print(points["30"][1])
# #print(convert_wgs_to_mercator(points))

# mercator_points = convert_wgs_to_mercator(points)


# -------------------------------XLXS----------------------------------------


# fichier avec les données
CSV_DATA_TARGET = "datas/POPULATION_MUNICIPALE_DEPARTEMENT_FRANCE.csv"
CSV_INDEX_NUM = 2  # index du num├®ro de d├®partement (INSEE) dans le fichier csv

def get_data_from_csv(filepath: str) -> dict:
    departements: dict = {}

    raw_datas: list = []
    with open(filepath, "r") as file:
        raw_datas = file.readlines()

    datas: List[List[str]] = [r.strip().split(',') for r in raw_datas]

    headers: List[str] = datas[0]  # titre des colonnes

    for departement in datas[1:]:
        departements[departement[CSV_INDEX_NUM]] = {}

        for i, titre in enumerate(headers):
            departements[departement[CSV_INDEX_NUM]][titre] = departement[i]

    departements["headers"] = headers
    return departements


def get_departement(departement: str) -> dict | None:
    res = get_data_from_csv(CSV_DATA_TARGET)
    if departement in res.keys():
        return res[departement]
    return None


headers = get_departement("headers")
departement = get_departement("75")


BLEU = "#42009E"
VIOLET = "#A30053"
ROSE = "#FF084B"
ORANGE = "#FF5A08"
JAUNE = "#FFC108"

def get_population_max(cle_annee = "p21_pop") -> int:
    num_dep = list(get_data_from_csv(CSV_DATA_TARGET).keys())
    num_dep.pop(-1)

    departements = get_data_from_csv(CSV_DATA_TARGET)
    
    curr_max = int(departements[num_dep[0]][cle_annee])
    num = 0
    while num < len(num_dep):
        pop_actuelle = int(departements[num_dep[num]][cle_annee])
        if pop_actuelle > curr_max:
            curr_max = pop_actuelle

        num += 1

    return curr_max



def get_population_min(cle_annee = "p21_pop") -> int:
    num_dep = list(get_data_from_csv(CSV_DATA_TARGET).keys())
    num_dep.pop(-1)

    departements = get_data_from_csv(CSV_DATA_TARGET)
    
    curr_min = int(departements[num_dep[0]][cle_annee])
    num = 0
    while num < len(num_dep):
        pop_actuelle = int(departements[num_dep[num]][cle_annee])
        if pop_actuelle < curr_min:
            curr_min = pop_actuelle

        num += 1

    return curr_min

def get_couleur(val: float, valeur_min: float, valeur_max: float) -> str:
    normalise =  (val - valeur_min) / (valeur_max - valeur_min)

    normalise *= 5
    return [JAUNE, ORANGE, ROSE, VIOLET, BLEU][int(normalise)]


epoque = 'p21_pop'
couleur = get_couleur(int(departement[epoque]), get_population_max(epoque), get_population_min(epoque))
print(couleur)