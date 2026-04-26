import pandas as pd
import warnings
warnings.filterwarnings('ignore')

print("Loading DataCo Supply Chain dataset...")
df = pd.read_csv(
    r'C:\Users\13142\Desktop\supply-chain-analytics\data\DataCoSupplyChainDataset.csv',
    encoding='latin-1'
)

print(f"\nShape: {df.shape}")
print(f"\nColumn names:")
for col in df.columns.tolist():
    print(f"  - {col}")

print(f"\nFirst 3 rows:")
print(df.head(3))

print(f"\nMissing values:")
print(df.isnull().sum()[df.isnull().sum() > 0])

print(f"\nData types:")
print(df.dtypes)

print("\nDone!")