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

def unify_tier(tier):
    try:
        return tier_conversions[tier]
    except KeyError:
        return tier

def merge_tiers():
    df = pd.read_csv(os.path.join("donnees", "dataset.csv"), index_col=False)

    df['tier'] = df['tier'].map(unify_tier)

    df.to_csv(os.path.join("donnees", "dataset2.csv"))