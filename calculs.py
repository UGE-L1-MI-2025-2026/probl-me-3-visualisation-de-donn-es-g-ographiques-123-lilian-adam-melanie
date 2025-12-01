from requirements import shapefile as shapefile
import typing
import pyexcel_xlsx as pyxl
import json
import math

#import shapefile

def wgs_to_mercator(pos, map_scale=1) -> typing.Tuple[float, float]:
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
    north, west, east, south = 0, 0, 0, 0
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
        if len(curr_record[0]) < 3: departments[curr_record[0]] = [curr_record[1], sf.shape(i).points]
    return departments




def calculate_distance(point1, point2):
    dist = point2[0]


def get_mercator_from_shp(file_name, map_size, map_scale=0.00005):
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
    distance = bbox_center[0] - map_center[0], bbox_center[1] - map_center[1]
    #scale = (get_distance((0, 0), (box[3], 0)))/map_size[0], (get_distance((0, 0), (0, box[1])))/map_size[1]
    scale = map_center[0]/bbox_center[0], map_center[1]/bbox_center[1]

    # bbox_center = wgs_to_mercator(get_center(bottom_left, up_right))
    # bbox_center = bbox_center[0]/(map_size[0]*map_size[1]), bbox_center[1]/(map_size[1]*map_size[0])
    # map_center = get_center((0, 0), (map_size[0], map_size[1]))
    # #distance = bbox_center[0] - map_center[0], bbox_center[1] - map_center[1]
    # distance = map_center[0] - bbox_center[0], map_center[1] - bbox_center[1]
    print(box, bbox_center, map_center, distance)

    mercator_points = convert_wgs_to_mercator(points, center= map_center, scale= scale, map_scale=map_size, distance=distance)
    return mercator_points


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
    

#sf = shapefile.Reader("departements-20180101-shp.zip/departements-20180101.shp")
#print(sf.records())
#print(sf.bbox)
#print(sf.shape(0))
#print(sf.record(0)[0])
#print(get_points(sf)["30"])

# sf = import_shp("departements-20180101-shp.zip/departements-20180101.shp")
# points = get_points(sf)
# #print(points["30"][1])
# #print(convert_wgs_to_mercator(points))

# mercator_points = convert_wgs_to_mercator(points)


# -------------------------------XLXS----------------------------------------


# def import_xlsx(file_name):
#     data = pyxl.get_data(file_name)
#     print(json.dump(data, dict)["III_1_insee_population_fr_depar"][0])

# import_xlsx("POPULATION_MUNICIPALE_DEPARTEMENT_FRANCE.xlsx")


# -------------------------------CSV----------------------------------------



