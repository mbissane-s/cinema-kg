import pandas as pd
from sklearn.model_selection import train_test_split

# load KG
df = pd.read_csv("../kg/kg_clean.csv")

# rename columns
df = df.rename(columns={
    "subject": "head",
    "predicate": "relation",
    "object": "tail"
})

# split data
train, temp = train_test_split(df, test_size=0.2, random_state=42)
valid, test = train_test_split(temp, test_size=0.5, random_state=42)

# save files (no header)
train.to_csv("train.txt", sep="\t", index=False, header=False)
valid.to_csv("valid.txt", sep="\t", index=False, header=False)
test.to_csv("test.txt", sep="\t", index=False, header=False)

print("KGE datasets created:")
print("train:", len(train))
print("valid:", len(valid))
print("test:", len(test))