import json, os, requests, time

BASE_URL = "https://pokeapi.co/api/v2/"
SELF_RATE_LIMIT = 0.1


def query(path: str, id: int) -> dict:
    """Fetch un objet de PokéAPI par son path et son id
    """
    try:
        request = requests.get(f"{BASE_URL}{path}{id}")
    except Exception as e:
        print (e)
        raise e
    
    dict = request.json()
    print(f"{request} : fetched data for {id}, {dict['name']}")
    return dict

def dump_pokemon(ids: list, path: str) -> None:
    """Écrit à un .json une liste de Pokémon de PokéAPI
    """

    api_dump = []

    # Try loop pour qu'on puisse au moins dump quelque-chose s'il-y-a un mauvais request
    try:
        for id in ids:
            dict = query("pokemon/", id)
            api_dump.append(dict)
            time.sleep(SELF_RATE_LIMIT) # PokéAPI ne rate limit pas donc on essaye d'être gentils
    except:
        print("Aborted dump")

    with open(path, "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)

    print(f"Wrote {len(api_dump)} pokémon to {path}")

def dump_moves(ids: list, path: str) -> None:
    """Écrit à un .json un dict des moves de PokéAPI
    """

    api_dump = {}

    # Try loop pour qu'on puisse au moins dump quelque-chose s'il-y-a un mauvais request
    try:
        for id in ids:
            dict = query("move/", id)
            api_dump[dict["name"]] = dict
            # Information TRÈS volumineuse pas nécessaire
            dict.pop("learned_by_pokemon")
    except:
        print("Aborted dump")

    with open(os.path.join(os.getcwd(), path), "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)
    
    print(f"Wrote {len(api_dump)} moves to {path}")

if __name__ == "__main__":
    all_pokemon_ids = list(range(1, 1026)) + list(range(10001, 10327))
    all_move_ids = list(range(1, 921))

    if not os.path.exists("raw_data"):
        os.mkdir("raw_data")

    dump_pokemon(all_pokemon_ids, os.path.join("raw_data", "dex.json"))
    dump_moves(all_move_ids, os.path.join("raw_data", "moves.json"))