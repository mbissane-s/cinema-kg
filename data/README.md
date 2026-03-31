# data/

## samples/

Pre-generated files for running the pipeline without internet access.

| File | Description |
|------|-------------|
| crawled_movies.csv | Raw Wikipedia infobox data (film, director, actor) |
| sparql.csv | DBpedia SPARQL query results with full URIs |
| kg_clean.csv | Cleaned triples (subject, predicate, object) |
| kg.ttl | RDF graph in Turtle format |

## kge/

Train/validation/test splits for Knowledge Graph Embedding.

| File | Triples |
|------|---------|
| train.txt | 303 |
| valid.txt | 38 |
| test.txt | 38 |

Format: tab-separated `head \t relation \t tail`, no header.
