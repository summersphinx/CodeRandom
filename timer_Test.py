import os
import pandas as pd

level = 'a little complicated'

dirPath = os.getcwd() + '/game'

wb = pd.read_excel(dirPath + '/levels/levels.xlsx', index_col='Level')
print(wb.keys())
print(type(wb))
print(wb)
var = wb.loc[level].values.tolist()
print(var)
print(type(var))
