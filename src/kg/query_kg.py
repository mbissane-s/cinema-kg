from rdflib import Graph

# load graph
g = Graph()
g.parse("kg.ttl", format="turtle")

# SPARQL query
query = """
PREFIX ex: <http://example.org/>

SELECT ?film ?actor
WHERE {
    ?film ex:actedIn ?actor .
}
LIMIT 10
"""

# execute query
results = g.query(query)

# print results
for row in results:
    print(f"Film: {row.film}, Actor: {row.actor}")