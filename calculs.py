from requirements import shapefile as shapefile
import typing
from typing import List, Any
#from pyexcel import get_sheet, Sheet
import json
import math

#import shapefile

def wgs_to_mercator_bis(pos, map_scale=1) -> typing.Tuple[float, float]:
    R : float = 6378137.000
    lat, lon = pos[0], pos[1]

    x = R * math.radians(lon)
    if lon != 0: scale = x / lon
    else: scale = x
    pi = math.pi
    y = 180 / pi * math.log(math.tan(pi/4.0 + lat * (pi/180.0)/2.0)) * scale

    x, y = x * map_scale, y * map_scale

    return (x, y)


def mercator_to_wgs():
    pass

def scale_point(point, center, scale):
    return scale * (point[0] - center[0]) + center[0], scale * (point[1] - center[1]) + center[1]


def convert_wgs_to_mercator(departments, center, scale, map_scale=(1,1) , distance=(0, 0)):
    departments_mercator : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }

    #map_scale = (map_scale[0] * map_scale[0], map_scale[1] * map_scale[1])

    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for curr_point in departments[department][1]:
            merc_curr_point = wgs_to_mercator(curr_point)
            new_point = scale[0] * (merc_curr_point[0] - center[0]) + center[0], scale[1] * (merc_curr_point[1] - center[1]) + center[1]
            #new_point = (merc_curr_point[0] + distance[0])/map_scale[0], (merc_curr_point[1] + distance[1])/map_scale[1]
            new_points.append(new_point)
        departments_mercator[department] = [ departments[department][0], new_points ]

    return departments_mercator


def import_csv(file_name):
    # csv
    pass


def import_netcdf(file_name):
    # module netCDF4
    pass


def get_distance(pos1, pos2) -> float:
    x, y = pos2[0] - pos1[0], pos2[1] - pos1[1]
    return math.sqrt(x*x + y*y)


def get_center(point1, point2) -> typing.Tuple[float, float]:
    return (point2[0] - point1[0])/2, (point2[1] - point1[1])/2


def scale_point(point, scale) -> typing.Tuple[float, float]:
    return point[0] * scale, point[1] * scale


def scale_points(departments, scale):
    departments_scaled : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }
    for department in departments:
        scaled_points : typing.List[typing.Tuple[float, float]] = [ ]
        for point in departments[department][1]:
            scaled_point = scale_point(point, scale)
            scaled_points.append(scaled_point)
        departments_scaled = [department] = [ departments[department][0], scaled_points ]

    return departments_scaled


def get_dist_corners_center():
    pass

"""
ALGO
get bbox
calculate center of bbox -> convert to mercator -> bbox_center
then:
calculate the center of the map (int, int) -> map_center
calculate the distance between the center of the map and the center of the bbox -> dist
dist: (float, float) dist btw map_center-bbox_center x, dist btw map_center-bbox_center y
for each polygon:
    for each point:
        convert to mercator the point
        point_x, point_y = point_x + dist[0], point_y + dist[1]

"""


def calculate_box(corners):
    west, south, east, north = corners[0][0][0], corners[0][0][1], corners[0][0][0], corners[0][0][1]
    print(west, south, east, north)
    for i in range(len(corners)):
        for point in corners[i]:
            if point[0] <= west: west = point[0]
            if point[0] >= east: east = point[0]
            if point[1] <= north: north = point[1]
            if point[1] >= south: south = point[1]

    return west, south, east,  north





# 29 finistère: ouest ; 59 nord: nord ; 2B haute-corse: est ; 2A corse-du-sud: sud


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

def get_points(sf, outremers= False) -> typing.Dict[str, int]:
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
        #if not(outremers) and len(curr_record[0]) < 3: departments[curr_record[0]] = [curr_record[1], sf.shape(i).points]
        if outremers and len(curr_record[0]) >= 3: continue
        else: departments[curr_record[0]] = [curr_record[1], sf.shape(i).points]
        
    return departments


"""
ALGO 2
get the corners coordinates (bounding box) of the mercator map
calculate the vertical and horizontal scale of the map based on the size of the window and the size of the mercator map
"""


def calculate_distance(point1, point2):
    dist = point2[0]


def get_mercator_from_shp_bis(file_name, map_size, map_scale=0.00005):
    """
    Parameters:
        map_size : typing.Tuple[int, int] = respectively the width and height of the map
    """
    sf = import_shp(file_name)
    #box = sf.bbox
    # bottom_left, up_right = (box[0], box[1]), (box[2], box[3])
    # diagonal = get_distance(bottom_left, up_right)
    points = get_points(sf)
    corners = points["29"][1], points["59"][1], points["2B"][1], points["2A"][1]
    box = calculate_box(corners)
    # map_center = get_center(map_size[0], map_size[1])
    #map_scale = 1/(distance * distance)

    bottom_left, up_right = (box[0], box[1]), (box[2], box[3])
    bbox_center = wgs_to_mercator(get_center(bottom_left, up_right))
    map_center = get_center((0, 0), (map_size[0], map_size[1]))

    bbox_diagonal = get_distance(wgs_to_mercator(bottom_left), wgs_to_mercator(up_right))
    map_diagonal = get_distance((0,0), map_size)
    distance = bbox_center[0] - map_center[0], bbox_center[1] - map_center[1]
    ##scale = (get_distance((0, 0), (box[3], 0)))/map_size[0], (get_distance((0, 0), (0, box[1])))/map_size[1]
    #scale = map_center[0]/bbox_center[0], map_center[1]/bbox_center[1]
    scale = map_diagonal/bbox_diagonal, map_diagonal/bbox_diagonal

    # bbox_center = wgs_to_mercator(get_center(bottom_left, up_right))
    # bbox_center = bbox_center[0]/(map_size[0]*map_size[1]), bbox_center[1]/(map_size[1]*map_size[0])
    # map_center = get_center((0, 0), (map_size[0], map_size[1]))
    # #distance = bbox_center[0] - map_center[0], bbox_center[1] - map_center[1]
    # distance = map_center[0] - bbox_center[0], map_center[1] - bbox_center[1]
    #print(box, bbox_center, map_center, distance, scale)

    mercator_points = convert_wgs_to_mercator(points, center= map_center, scale= scale, map_scale=map_size, distance=distance)
    return mercator_points


def try_stuff(file_name, map_size):
    sf = import_shp(file_name)
    points = get_points(sf)
    corners = calculate_box(points) # west, south, east,  north
    bottom_left, up_right = (corners[0], corners[1]), (corners[2], corners[3])
    distance_bl, distance_ur = get_distance((0, 0), bottom_left), get_distance((map_size, up_right))


def do_everything(departments, box, map_size):
    departments_mercator : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }

    bottom_left, up_right = (box[0], box[1]), (box[2], box[3])
    bbox_center = wgs_to_mercator(get_center(bottom_left, up_right))
    map_center = get_center((0, 0), (map_size[0], map_size[1]))
    distance = bbox_center[0] - map_center[0], bbox_center[1] - map_center[1]
    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for curr_point in departments[department][1]:
            merc_curr_point = wgs_to_mercator(curr_point)
            new_point = merc_curr_point[0] + distance[0], merc_curr_point[1] + distance[1]
            new_points.append(new_point)
        departments_mercator[department] = [ departments[department][0], new_points ]

    return departments_mercator


from math import log, tan, pi, radians, degrees

def mercator(long, lat):
    x = long
    y = degrees(log(tan(radians(lat) / 2 + pi / 4)))
    return x, y


def calcule_parametres(x_min, y_min, x_max, y_max, x_orig, y_orig, W, H): # -> (a, B, C)
    # a: scale; B = décalage des abscisse, C = décalage des ordonnées

    a_abscisses =  W / (x_max - x_min)
    a_ordonnees = H / (y_max - y_min)
    a = min(a_abscisses, a_ordonnees)

    B = x_orig - (a * x_min)
    C = y_orig + (a * y_min)

    return a, B, C

#place_point = lambda x, y, a, B, C: (a * x + B, -a * y + C)
def place_point(x, y, a, B, C):
    return (a*x) + B, ((0-a)*y) + C


def wgs_to_mercator_bis(departments, scale, x_offset, y_offset):
    departments_mercator : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }

    #map_scale = (map_scale[0] * map_scale[0], map_scale[1] * map_scale[1])

    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for curr_point in departments[department][1]:
            merc_curr_point = mercator(curr_point[0], curr_point[1])
            placed_point = place_point(merc_curr_point[0], merc_curr_point[1], scale, x_offset, y_offset)
            new_points.append(placed_point)
        departments_mercator[department] = [ departments[department][0], new_points ]

    return departments_mercator


def wgs_to_mercator(departments):
    departments_mercator : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }

    #map_scale = (map_scale[0] * map_scale[0], map_scale[1] * map_scale[1])

    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for curr_point in departments[department][1]:
            merc_curr_point = mercator(curr_point[0], curr_point[1])
            new_points.append(merc_curr_point)
        departments_mercator[department] = [ departments[department][0], new_points ]

    return departments_mercator


def place_all_points(departments, scale, x_offset, y_offset, width, height):
    new_departments : typing.Dict[str, typing.List[str, typing.List[typing.Tuple[float, float]]]] = {

    }
    for department in departments:
        new_points : typing.List[typing.Tuple[float, float]] = [ ]
        for curr_point in departments[department][1]:
            new_point = place_point(curr_point[0], curr_point[1], scale, x_offset, y_offset)
            new_point = new_point[0], height + new_point[1]
            new_points.append(new_point)
        new_departments[department] = [ departments[department][0], new_points ]
    return new_departments


def separate_isles(sf, departments):
    departments["isles"] = ["isles"]
    #for shape in sf.shapes()
    sf_parts = sf.parts()




def get_mercator_from_shp(file_name, map_size):
##    width, height = map_size[0], map_size[1]
##    sf = import_shp(file_name)
##    points = get_points(sf)
##    corners = calculate_box(points) # west, south, east,  north
##    bottom_left, up_right = (corners[0], corners[1]), (corners[2], corners[3])
##    dist_boxh = get_distance((0,0), (0, corners[1]))
##    dist_maph = get_distance((0,0), (0, height))
##    dist_boxw = get_distance((0,0), (corners[2], (0,0)))
##    dist_mapw = get_distance((0,0), (0, height))
##    #scale = dist_box/dist_map



    outremers = True
    sf = import_shp(file_name)
    points = get_points(sf, outremers)
    prep_corners = points["29"][1], points["59"][1], points["2B"][1], points["2A"][1]
    print(prep_corners[0])
    corners = calculate_box(prep_corners) # west, south, east,  north
    #bottom_left, up_right = (corners[0], corners[1]), (corners[2], corners[3])
    (x_min, y_min), (x_max, y_max) = (corners[0], corners[3]), (corners[2], corners[1])
    #print(points)

    width, height = map_size[0], map_size[1]
    box_x_min, box_y_min, box_x_max, box_y_max = sf.bbox

    if not(outremers):
        if box_x_min <= x_min: x_min = box_x_min
        if box_y_min <= y_min: y_min = box_y_min
        if x_max <= box_x_max: x_max = box_x_max
        if y_max <= box_y_max: y_max = box_y_max

    (x_min_merc, y_min_merc), (x_max_merc, y_max_merc) = mercator(x_min, y_min), mercator(x_max, y_max)

    scale, x_offset, y_offset = calcule_parametres(x_min_merc, y_min_merc, x_max_merc, y_max_merc, 0, 0, width, height)
    print(scale, x_offset, y_offset)
    departments_mercator = wgs_to_mercator(points)
    placed_departments = place_all_points(departments_mercator, scale, x_offset, y_offset, width, height)
    #print(departments_mercator == placed_departments)

    return placed_departments


    # width_adj, height_adj = width/(x_max - x_min), height/(y_max - y_min)
    # scale = min(width_adj, height_adj)

    # if scale == width_adj: width_adjust = width_adj
    # if scale == height_adj: height_adjust = height_adj



    #scale = min(W/(x2-x1), H/(y1-y2))
    #si scale = W/(x2-x1), B = X0 - ax1
    #si scale = H/(y1-y2), C = Y0 + ay1



#homothétie




#sf = shapefile.Reader("departements-20180101-shp/departements-20180101.shp")
#print(sf.records())
#print(sf.bbox)
#print(get_points(sf))
#print(sf.shape(0))
#print(sf.record(0)[0])
#print(get_points(sf)["30"])

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

# source: https://coolors.co/palette/ff4800-ff5400-ff6000-ff6d00-ff7900-ff8500-ff9100-ff9e00-ffaa00-ffb600
PALETTE_COULEURS = [
    "#03071E",
    "#370617",
    "#6A040F",
    "#9D0208",
    "#D00000",
    "#DC2F02",
    "#E85D04",
    "#F48C06",
    "#FAA307",
    "#FFBA08"
]

def get_couleur(val: float, valeur_min: float, valeur_max: float, couleurs: list = None) -> str:
    normalise =  (val - valeur_min) / (valeur_max - valeur_min)
    normalise *= len(couleurs)
    normalise = int(normalise)
    normalise = min(normalise, len(couleurs)-1)

    if couleurs == None:
        couleurs = [JAUNE, ORANGE, ROSE, VIOLET, BLEU]

    return couleurs[normalise]


HEADER_INDEX_POP = 5


def main():
    headers = get_departement("headers")
    
    departement = get_departement("75")
    print(departement["nom_dep"])


    epoques = headers[5:]
    for epoque in epoques:
        couleur = get_couleur(int(departement[epoque]), get_population_max(epoque), get_population_min(epoque), PALETTE_COULEURS)
        print(
            f"{epoque = }"
            f"population: {departement[epoque]}, couleur = {couleur}"
        )



    print("=" * 100)


    departement = get_departement("94")
    print(departement["nom_dep"])


    epoques = headers[5:]
    for epoque in epoques:
        couleur = get_couleur(int(departement[epoque]), get_population_max(epoque), get_population_min(epoque), PALETTE_COULEURS)
        print(
            f"{epoque = }"
            f"population: {departement[epoque]}, couleur = {couleur}"
        )




if __name__ == "__main__":
    main()