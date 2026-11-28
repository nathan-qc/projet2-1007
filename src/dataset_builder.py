import json, os, csv
import merge_tiers

with open(os.path.join("raw_data", "moves.json"), "r", encoding="utf-8") as f:
    MOVES: dict = json.load(f)

with open(os.path.join("raw_data", "dex.json"), "r", encoding="utf-8") as f:
    DEX: dict = json.load(f)

with open(os.path.join("donnees", "tiers.csv"), "r", encoding="utf-8") as f:
    r = csv.reader(f)
    next(r)             # éliminer l'en-tête
    TIERS = dict(r)


def build_row(mon:dict)->tuple:
    """Prend un dict de Pokémon selon le format de PokéAPI et construit la rangée correspondante pour le .csv, sans le tier
    """
    # Pour notre propre usage, ne sera pas traité par le modèle
    name = mon["name"]

    # Numéro du pokémon dans le pokédex (en ordre de sortie)
    dex_id = mon["id"]

    # Types du pokémon, none à type_2 si il n'a qu'un seul type
    type_1 = mon["types"][0]["type"]["name"]
    type_2 = mon["types"][1]["type"]["name"] if len(mon["types"]) == 2 else "none"

    # Stats du pokémon (https://bulbapedia.bulbagarden.net/wiki/Stat)
    [hit_points, attack, defense, special_attack, special_defense, speed] = [stat["base_stat"] for stat in mon["stats"]]

    # Nombre de types uniques dans les moves du pokémon
    coverage = []

    # Puissance de son move le plus puissant
    max_power = 0

    # Nombre de status moves (https://bulbapedia.bulbagarden.net/wiki/Status_move)
    n_status_moves = 0

    for move in mon["moves"]:
        move_name = move["move"]["name"]

        # On regarde chaque dict qui représente les versions du jeu ou le pokémon apprend le move en question
        for version in move["version_group_details"]:
            # On get le nom de cette version
            version_name = version["version_group"]["name"]
            # Si c'est scarlet-violet, algors on traite le move
            if version_name == "scarlet-violet":
                # Si le move est un status move, alors on le compte dans le total de status moves
                if MOVES[move_name]["damage_class"]["name"] == "status":
                    n_status_moves += 1
                # Si c'est pas un status move, alors il a (la plupart du temps) un power
                # Certain moves de dégâts ont un power variable en combat, donc ils n'ont pas de valeur de power
                elif MOVES[move_name]["power"]:
                    # On ajoute le type du move a coverage
                    coverage.append(MOVES[move_name]["type"]["name"])
                    # Si c'est plus puissant que l'ancien move le plus puissant, on change
                    max_power = max(max_power, MOVES[move_name]["power"])
                break

    # On aura des types répétés, donc on fait un set avant de get le nombre de types uniques
    coverage_count = len(set(coverage))

    return (name, dex_id, type_1, type_2, hit_points, attack, defense, special_attack, special_defense, speed, coverage_count, max_power, n_status_moves)

def append_tiers(path_out: str)->None:
    """Construit le dataset et ajoute les tiers à chaque rangée, puis exporte le dataset à un .csv
    """
    dataset = list()

    for mon in DEX:
        
        if mon["name"] in TIERS:
            row = build_row(mon) + (TIERS[mon["name"]],)
            dataset.append(row)

    with open(path_out, "w", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(("name", "id", "type_1", "type_2", "hp", "atk", "def", "spa", "spd", "spe", "coverage", "power", "status", "tier"))
        w.writerows(dataset)

if __name__ == "__main__":
    append_tiers(os.path.join("donnees", "dataset3.csv"))
    merge_tiers.merge_tiers(os.path.join("donnees", "dataset3.csv"), os.path.join("donnees", "dataset6.csv"))