from rdflib import Graph, URIRef, Namespace
import pandas as pd

# load cleaned data
df = pd.read_csv("kg_clean.csv")

# create graph
g = Graph()

# namespace
EX = Namespace("http://example.org/")

for _, row in df.iterrows():
    s = URIRef(EX[row["subject"].replace(" ", "_")])
    p = URIRef(EX[row["predicate"]])
    o = URIRef(EX[row["object"].replace(" ", "_")])

    g.add((s, p, o))

# save RDF
g.serialize("kg.ttl", format="turtle")

print("RDF graph created: kg.ttl")