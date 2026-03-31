import pandas as pd

# load csv
df = pd.read_csv("../data/sparql.csv")

# function to clean URI
def clean_uri(uri):
    if isinstance(uri, str):
        return uri.split("/")[-1].replace("_", " ")
    return uri

# apply cleaning
df["film"] = df["film"].apply(clean_uri)
df["director"] = df["director"].apply(clean_uri)
df["actor"] = df["actor"].apply(clean_uri)

# remove duplicates
df = df.drop_duplicates()

# create triples
triples = []

for _, row in df.iterrows():
    triples.append((row["film"], "directedBy", row["director"]))
    triples.append((row["film"], "actedIn", row["actor"]))

# remove duplicates again
triples = list(set(triples))

# convert to dataframe
kg_df = pd.DataFrame(triples, columns=["subject", "predicate", "object"])

# save
kg_df.to_csv("kg_clean.csv", index=False)

print(kg_df.head())