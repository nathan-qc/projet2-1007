import json, os, requests, time

BASE_URL = "https://pokeapi.co/api/v2/"
SELF_RATE_LIMIT = 0.1
OUTPUT_FILEPATH = "api_dump.json"

def query_pokemon(id: int) -> dict:
    """Fetch un pokémon de PokéAPI par son id
    """
    request = requests.get(f"{BASE_URL}pokemon/{id}")
    pokemon_dict = request.json()
    print(f"{request} : fetched data for {pokemon_dict['name']} (dex #{pokemon_dict['id']})")
    return pokemon_dict

def dump_pokemons(ids: list = []) -> None:
    """Écrit à un .json une liste de dict de pokémon
    """

    api_dump = []

    # Try loop pour qu'on puisse au moins dump quelque-chose s'il-y-a un mauvais request
    try:
        for id in ids:
            pokemon = query_pokemon(id)
            api_dump.append(pokemon)
            time.sleep(SELF_RATE_LIMIT) # PokéAPI ne rate limit pas donc on essaye d'être gentils
    except:
        pass

    with open(os.path.join(os.getcwd(), OUTPUT_FILEPATH), "w", encoding="utf-8") as f:
        json.dump(api_dump, f, indent=2)

    print(f"Wrote {len(api_dump)} pokémon to {OUTPUT_FILEPATH}")