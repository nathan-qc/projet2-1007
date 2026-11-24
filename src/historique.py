import os, csv

PATH = "historique.csv"

def init_hist():
    with open(PATH, "w", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "type_1", "type_2", "hp", "atk", "spa", "def", "spd", "spe", "coverage", "power", "status", "tier"])

def get_hist()->list[list]:
    data = []
    if os.path.isfile(PATH):
        with open(PATH, "r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for line in reader:
                data.append(line)
    return data

def hist_add_row(id:int, type_1:str, type_2:str, hp:int, attack:int, special_attack:int, defense:int, special_defense:int, speed:int, coverage:int, power:int, status:int, tier:int)->str:
    data = get_hist()
    data.append([id, type_1, type_2, hp, attack, special_attack, defense, special_defense, speed, coverage, power, status, tier])
    if os.path.isfile(PATH):
        with open(PATH, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            for line in data:
                writer.writerow(line)

init_hist()