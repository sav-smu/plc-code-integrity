import os
import pandas as pd
input__path=os.path.abspath('..')+"\data\\22June2020_B.csv"
df=pd.read_csv(input__path)
print (df.head())


print (df.columns)