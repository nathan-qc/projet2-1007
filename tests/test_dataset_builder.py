import sys
sys.path.append("src")
import os, json
from dataset_builder import build_row

PATH = os.path.join("tests", "test_data.json")

if os.path.isfile(PATH):
    with open(PATH, "r", encoding="utf-8") as f:
        DATA = json.load(f)

# Cas normal
def test_row_bulbasaur():
    mon = DATA[0]
    assert build_row(mon) == ('bulbasaur', 1, 'grass', 'poison', 45, 49, 49, 65, 65, 45, 4, 130, 21)

# Shuckle n'existe pas dans SV, donc puisqu'il n'a aucun move de noté comme appris dans SV, les 3 dernières
# valeurs qui sont en lien avec les moves doivent être 0
def test_row_shuckle():
    mon = DATA[1]
    assert build_row(mon) == ('shuckle', 213, 'bug', 'rock', 20, 10, 230, 10, 230, 5, 0, 0, 0)

# Cosmog n'apprends aucun move qui fait des dégats, donc son coverage et son power devraient être 0
# (avant et avant avant dernière valeurs)
# Cosmog a aussi un seul type, donc on verifie ca ici
def test_row_cosmog():
    mon = DATA[2]
    assert build_row(mon) == ('cosmog', 789, 'psychic', 'none', 43, 29, 31, 29, 31, 37, 0, 0, 2)

# Kyurem Black est une forme spéciale, donc son id n'est pas son pokédex number mais plutot un id determiné par
# PokéAPI. On veut donc vérifier que notre fonction prends cet id et non une autre variable tel que le dex id du
# pokémon à la base de la forme spéciale.
def test_row_kyurem_black():
    mon = DATA[3]
    assert build_row(mon) == ('kyurem-black', 10022, 'dragon', 'ice', 125, 170, 100, 120, 90, 95, 11, 150, 17)