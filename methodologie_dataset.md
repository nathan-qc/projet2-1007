# Méthodologie de la conception du dataset
## Considerations initiales
Pour obtenir les données sur les pokémon, nous avons utilisé PokéAPI (pokeapi.co). Ces données sont en .json et contiennent beaucoup plus d'information que ce dont nous avons besoin.

Nous avons tiré nos informations comme suit: pour le URL "https://pokeapi.co/api/v2/pokemon/[ID_HERE]", nous avons pris tous les pokémon de ID 1 à 1025 (inclusivement), ce qui représente l'ensemble du pokédex "normal". Nous avons ensuite pris tous les pokémon de ID 10001 à 10326 (inclusivement), ce qui représente l'ensemble des formes différentes de certains pokémon dans le pokedex. Des exemples de ces différences de formes sont:
- Pour lycanroc-midday dans le pokédex "normal", il-y-a lycanroc-dusk dans l'ensemble des formes
- Pour pikachu dans le pokédex "normal", il-y-a pikachu-rock-star dans l'ensembles des formes

Dans le cas de Lycanroc, ce pokémon a une "forme" midday et dusk. Ces formes ont des abilités différentes, ce qui constitue assez pour que Smogon les considère uniques (même s'ils sont dans le même usage tier au final). Pour Pikachu, Pikachu Rock Star est une forme spéciale qui apprends un seul move que Pikachu n'apprends pas normalement. Cependant, ce Pokémon n'existe pas dans SV. On doit donc faire un travail de vérification manuelle avec les données obtenues entre les ID 10000 et 100326 pour s'assurer qu'on n'inclus pas des pokémons qui n'existent pas dans SV. Un exemple est les mega-evolutions, qui n'existent pas dans SV.

Sur le sujet des pokémon qui n'existent pas dans SV, certains de pokémon dans le pokédex "normal" ne sont pas dans SV, par exemple Togekiss (id 468). Nous devrons enlever ces pokémon.

## Choix concrets