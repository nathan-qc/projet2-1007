import json, os, requests, time

BASE_URL = "https://pokeapi.co/api/v2/"
SELF_RATE_LIMIT = 0.1
OUTPUT_FILEPATH = "api_dump.json"

def query(path: str, id: int) -> dict:
    """Fetch un objet de PokéAPI par son path et son id
    """
    request = requests.get(f"{BASE_URL}{path}{id}")
    dict = request.json()
    print(f"{request} : fetched data for {dict['name']}")
    return dict

def dump_pokemon(ids: list = []) -> None:
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
        pass

    with open(os.path.join(os.getcwd(), OUTPUT_FILEPATH), "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)

    print(f"Wrote {len(api_dump)} pokémon to {OUTPUT_FILEPATH}")

def dump_moves(ids: list = []) -> None:
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
        pass

    with open(os.path.join(os.getcwd(), OUTPUT_FILEPATH), "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)
    
    print(f"Wrote {len(api_dump)} moves to {OUTPUT_FILEPATH}")