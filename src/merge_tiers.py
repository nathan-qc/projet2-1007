import pandas as pd
import os

tier_conversions = {
    'ag': 'uber',
    'uubl': 'ou',
    'rubl': 'uu',
    'nubl': 'ru',
    'publ': 'nu',
    'zubl': 'pu',
}

def unify_tier(tier:str)->str:
    """Prends un tier et retourne le tier auquel il se fait merge
    """
    try:
        return tier_conversions[tier]
    except KeyError:
        return tier

def merge_tiers(path_in: str, path_out: str)->None:
    """Ouvre le database et applique tout les consolidations de tier
    """
    df = pd.read_csv(path_in, index_col=False)

    df['tier'] = df['tier'].map(unify_tier)

    df.to_csv(path_out)