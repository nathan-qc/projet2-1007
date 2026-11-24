from predictor import Predictor
import pandas as pd
import matplotlib.pyplot as plt

class Engine():
    """Un wrapper autour d'un Predictor avec une seule méthode, confidences, qui est utilisée pour l'affichage des résultats"""
    def __init__(self, name):
        self.p = Predictor(name)

    def confidences(self, dex, type_1, type_2, hp, atk, defense, spa, spd, spe, coverage, power, status):
        """À utiliser par le UI. Avec les données d'un pokemon en entrée, ceci retourne le tier prédit ainsi que la confiance en celui-ci, en plus d'une figure matplotlib représentant les autre option."""

        X = pd.DataFrame(
            [[dex, type_1, type_2, hp, atk, defense, spa, spd, spe, coverage, power, status]],
            columns=['dex','type_1', 'type_2', 'hp', 'atk', 'def', 'spa', 'spd', 'spe', 'status', 'power', 'coverage']
        )


        # Création de deux tuples, un des probabilités en ordre croissant et un des noms de tiers, associés à la probabilité au même index
        likely_per_tier = map(lambda f: float(f) ,self.p.predict_tier(X)[0])
        associated = list(zip(likely_per_tier, self.p.le.classes_))
        sort = sorted(associated)
        final = list(zip(*sort))

        probas = final[0]
        labels = final[1]

        # Création du graphique à afficher dans le UI
        fig, ax = plt.subplots()
        ax.set_title("Distribution des probabilités")
        ax.barh(labels, probas)
        ax.set_xlim(0, 1)

        plt.show()

        return (labels[-1], probas[-1], fig)


if __name__ == "__main__":
    e = Engine("two")
    # print(e.confidences(1,"grass","poison",45,49,49,65,65,45,4,130,21))
    print(e.confidences(496,"grass","none",60,60,75,60,75,83,6,130,22))
    