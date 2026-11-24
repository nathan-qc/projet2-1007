import joblib
import os


class Predictor:
    def __init__(self, name):

        path = os.path.join("modeles", name + ".joblib")
        dict = joblib.load(path)

        self.model = dict["model"]
        self.le = dict["le"]

    def predict_tier(self, X):
        """Prend un tableau de données de Pokemon en entrée et retourne les probabilité quil soit dans chaque tier"""
        return self.model.predict_proba(X)

    

if __name__ == "__main__":
    from dataset import Dataset

    d = Dataset("dataset2")
    X = d.X.iat[0]

    p = Predictor("one")

    print(p.predict_tier(X))
    print(p.le.classes_)



