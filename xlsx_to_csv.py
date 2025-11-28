from pyexcel import get_sheet

target = "datas/POPULATION_MUNICIPALE_DEPARTEMENT_FRANCE.xlsx"
dest = "datas/POPULATION_MUNICIPALE_DEPARTEMENT_FRANCE.csv"

s = get_sheet(file_name=target, name_columns_by_row=0)
s.save_as(dest)
print(f"fichier xlsx converti en csv au chemin: {dest}")