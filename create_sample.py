import pandas as pd
import os

df = pd.read_csv(
    r'C:\Users\13142\Desktop\supply-chain-analytics\data\DataCoSupplyChainDataset.csv',
    encoding='latin-1',
    nrows=50000
)
df.to_csv('data/supply_chain_sample.csv', index=False, encoding='utf-8')
print(f"Sample created: {len(df):,} rows")
print(f"Size: {os.path.getsize('data/supply_chain_sample.csv')/1024/1024:.1f} MB")
