# Projet 2: de la donnée à l'application
*INF1007 gr. 04*\
*Nathan Vallée-Wilson (2544693) et Rémi Coulombe (2545018)*

Notre projet consiste à un modèle qui prédit a quel point un pokémon fictif serait bon en pokémon compétitif. Un des formats les plus populaires de pokémon compétitif s'agit des "singles", les combats 1 contre 1. Ce format est pratiqué en grande partie sur le site https://pokemonshowdown.com/ et est régi par https://www.smogon.com/. Le format est divisé en "tiers", des paliers définis par l'usage d'un pokémon qui limitent ceux qu'on peut utiliser. Ces tiers sont [1]:

- Anything Goes
- Uber
- OU : OverUsed
- UU (et UUBL) : UnderUsed
- RU (et RUBL) : RarelyUsed
- NU (et NUBL) : NeverUsed
- PU (et PUBL) : PoorlyUsed
- ZU (et ZUBL) : ZeroUsed
- NFE : Not Fully Evolved
- LC : Little Cup

Certains des formats ont une "banlist". Par exemple UUBL est l'ensemble des pokémons trop bons pour UU, donc qui y sont bannis, mais qui ne sont pas assez bons pour OU [2].

Notre projet vise a prédire dans quel tier un pokémon se retrouverait grace a un modèle de [STRATÉGIE UTILISÉE] entrainé sur un dataset comprennant tous le pokémons legaux dans les formats singles pour les jeux Pokémon Scarlet et Violet. 

## Jeu de données
Nos variables sont:

- Le numéro de pokédex. (quantitative)
- Le premier type du pokémon. (qualitative)
- Le deuxième type du pokémon, `aucun` s'il est monotype (qualitative)
- HP, les PV du pokémon. (quantitative)
- ATK, la stat d'attaque physique du pokémon. (quantitative)
- DEF, la stat de défense physique du pokémon. (quantitative)
- SPA, la stat d'attaque spéciale du pokémon. (quantitative)
- SPD, la stat de défense spéciale du pokémon. (quantitative)
- SPE, la stat de vitesse du pokémon. (quantitative)
- Coverage, le nombre de types uniques parmis les attaques du pokémon (quantitative)
- Power, la puissance la plus élevée parmis les attaques du pokémon (quantitative)
- Status, le nombre d'attaque de statut (qui ne font pas de dégâts et ont plutot un effet spécial) du pokémon (quantitative)

Nos données contiennent aussi les noms de chaque pokémon, chose qui n'est pas utilisé dans le modèle. Nous l'avons ajouté pour rendre les données plus lisibles.

Nous avons conçu notre jeu de données à partir de l'API "PokéAPI" et de Smogon [3][4]. Nos données de tiers de Smogon sont en date du retiering de octobre 2026 [5]. PokéAPI a la license BSD 3-Clause, qui permet l'usage en autant que la license est ajoutée au projet [6]. Les statistiques d'usage de Smogon n'ont pas de license explicite, mais sont disponible publiquement et utilisées de manière transformative régulièrement par la communauté.

Nous avons décidé de consolider certains tiers pour augmenter la taille d'échantillon associée à chaque tier. Les consolidations sont comme suit:

- Anything Goes → Uber
- UUBL → OU
- RUBL → UU
- NUBL → RU
- PUBL → NU
- ZUBL → PU

Anything Goes ne contient que 2 pokémons, qui sont bannis en Uber, donc c'est un tier peu pertinent à prédire. Pour les banlist, nous les avons ajouté au tier le plus bas sur l'échelle dans lequel ils sont légaux, afin d'augmenter la taille d'échantillon des tiers.

## L'interface graphique
Notre choix de technologie pour l'interface graphique est Gradio [7]. 

## Outil de fonctions complexes
TODO

## Couverture
TODO

## Références

[1] Smogon. (2026) Formats. [En ligne]. Disponible: https://www.smogon.com/dex/sv/formats/ (consulté le 23 novembre 2026)\
[2] Smogon. (2026) UUBL. [En ligne]. Disponible: https://www.smogon.com/dex/sm/formats/uubl/ (consulté le 23 novembre 2026)\
[3] PokéAPI. (2026) PokéAPI. [En ligne]. Disponible: https://pokeapi.co/ (consulté le 23 novembre 2026)\
[4] Smogon. (2026) Pokemon. [En ligne]. Disponible: https://www.smogon.com/dex/sv/pokemon/ (consulté le 11 novembre 2026)\
[5] Marty. (2026) Usage-Based Tier Update for October 2026 (November @ #19). [En ligne]. Disponible: https://www.smogon.com/forums/threads/usage-based-tier-update-for-october-2026-november-19.3789169/ (consulté le 23 novembre 2026)\
[6] P. Hallet. (2023) LICENSE.md. [En ligne]. Disponible: https://github.com/PokeAPI/pokeapi/blob/master/LICENSE.md (consulté le 23 novembre 2026)\
[7] Gradio. (2026) API Reference. [En ligne]. Disponible: https://gradio.app/docs (consulté le 23 novembre 2026)