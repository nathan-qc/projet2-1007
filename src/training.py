from models import LogisticReg
from dataset import Dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

d = Dataset("dataset2")
r = LogisticReg(d)

preds = pd.DataFrame(r.benchmark())
preds["y"] = d.y

def f(series):
    ps: list = series.to_list()[:-1]

    i_max = np.array(ps).argmax()
    
    target = int(series.to_list()[-1])
    confidence = ps[target]
    correct = i_max == target

    return [confidence, target, correct]

confidences = preds.apply(f, axis=1)

accurates = list(zip(*[c[0:2] for c in confidences if c[2]]))
innaccurates = list(zip(*[c[0:2] for c in confidences if not c[2]]))

# transpose = list(zip(*confidences))
# colormap = np.array(['r', 'g'])

# print(transpose[2])

plt.scatter(accurates[1], accurates[0], c="green")
plt.scatter(innaccurates[1], innaccurates[0], c="red")

plt.show()