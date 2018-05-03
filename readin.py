import pandas as pd
df = pd.read_excel('SwiftSNWeblist.xlsx','FullSNList',header = 1, parse_col = 9)
print(df)
print(df['ra'])