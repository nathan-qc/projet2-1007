import json, os, requests, time

BASE_URL = "https://pokeapi.co/api/v2/"
SELF_RATE_LIMIT = 0.01
OUTPUT_FILEPATH = "api_dump.json"

def query_pokemon(id):
    request = requests.get(f"{BASE_URL}pokemon/{id}")
    pokemon_json = request.json()
    print(f"{request} : fetched data for {pokemon_json["name"]} (dex #{pokemon_json["id"]})")
    return pokemon_json

def get_dex(start = 1, end = None):
    end = start + 1 if not end else end + 1

    api_dump = []
    try:
        for id in range(start, end):
            pokemon = query_pokemon(id=id)
            api_dump.append(pokemon)
            time.sleep(SELF_RATE_LIMIT)
    except:
        pass

    with open(os.path.join(os.getcwd(), OUTPUT_FILEPATH), "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)
    print(f"Wrote {len(api_dump)} pokémon to {OUTPUT_FILEPATH}")