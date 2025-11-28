from requirements import shapefile as shapefile
import typing
import pyexcel_xlsx as pyxl
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


# def import_xlsx(file_name):
#     data = pyxl.get_data(file_name)
#     print(json.dump(data, dict)["III_1_insee_population_fr_depar"][0])

# import_xlsx("POPULATION_MUNICIPALE_DEPARTEMENT_FRANCE.xlsx")


# -------------------------------CSV----------------------------------------



