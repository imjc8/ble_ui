import pandas as pd
import matplotlib.pyplot as plt
from time import sleep

def count_to_float(count, vref, bits):
    return vref/(2**bits - 1) *count 

df = pd.read_csv("data.csv")
#plt.stem(df.iloc[:,0],linefmt="")

dac_count =  df.iloc[:,0].to_numpy()
adc_count = df.iloc[:,1].to_numpy()

dac = count_to_float(dac_count,3.3,12)
adc = count_to_float(adc_count,3.3,11)

plt.plot(adc_count)
plt.show()