import pandas as pd
import os
import matplotlib.pyplot as plt

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

df = pd.read_csv(os.path.join("donnees", "dataset.csv"), index_col=False)

df['tier'] = df['tier'].map(unify_tier)

df.to_csv(os.path.join("donnees", "dataset2.csv"))

# groupes = df.groupby('tier')
# trend = groupes.size()
# plt.bar(range(15), trend)
# plt.title("tiers")
# plt.show()