from requirements import shapefile as shapefile
import typing
#import shapefile

def wgs_to_mercator():
    pass


def mercator_to_wgs():
    pass


def import_csv(file_name):
    # csv
    pass


def import_netcdf(file_name):
    # module netCDF4
    pass


# -------------------------------SHAPEFILE----------------------------------------


def import_shp(file_name) -> shapefile:
    # shapefile
    sf : shapefile = shapefile.Reader(file_name)

    return sf

def get_points(sf) -> typing.Dict[str, int]:
    departements : typing.Dict[str, int] = {

    }
    sf_shapes = sf.shapes()

    for i in range(len(sf_shapes)):
        curr_record = sf.record(i)
        departements[curr_record[0]] = [curr_record[1], sf.shape(i).points]
    return departements
    

sf = shapefile.Reader("departements-20180101-shp.zip/departements-20180101.shp")
print(sf.records())
print(sf.shape(0))
print(sf.record(0)[0])
print(get_points(sf)["30"])
