import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")
plt.stem(df.iloc[:,0],linefmt="")
plt.show()