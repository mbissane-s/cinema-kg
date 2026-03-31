# Cinema Knowledge Graph

Knowledge Graph in the cinema domain, built from Wikipedia infoboxes.
Covers films, directors, and actors — with RDF modeling, DBpedia alignment,
SWRL reasoning, KGE training, and a SPARQL-based RAG assistant.

---

## Project structure
```
project-root/
├── src/
│   ├── crawl/      crawler.py
│   ├── ie/         ner.py
│   ├── kg/         build_kg.py  to_rdf.py  query_kg.py
│   ├── reason/     swrl_rules.py
│   ├── kge/        prepare_kge.py  simple_kge.py  train_kge.py
│   └── rag/        rag_demo.py
├── data/
│   ├── samples/    crawled_movies.csv  sparql.csv  kg_clean.csv  kg.ttl
│   ├── kge/        train.txt  valid.txt  test.txt
│   └── README.md
├── kg_artifacts/
│   ├── ontology.ttl
│   ├── expanded.nt
│   └── alignment.ttl
├── reports/
│   └── final_report.pdf
├── notebooks/
│   └── cinema_demo.ipynb
├── README.md
├── requirements.txt
├── .gitignore
└── LICENSE
```

---

## Installation

Python 3.9+ required.
```bash
git clone https://github.com/mbissane-s/cinema-kg.git
cd cinema-kg
python3 -m pip install -r requirements.txt
```

---

## How to run each module

All commands run from `project-root/`.

**1. Crawl Wikipedia infoboxes**
```bash
python3 src/crawl/crawler.py
# → data/samples/crawled_movies.csv
```

**2. NER and entity cleaning**
```bash
python3 src/ie/ner.py
# → data/samples/crawled_movies_clean.csv
```

**3. Build the KG triples (CSV)**
```bash
python3 src/kg/build_kg.py
# → data/samples/kg_clean.csv
```

**4. Convert to RDF**
```bash
python3 src/kg/to_rdf.py
# → data/samples/kg.ttl
```

**5. SPARQL queries**
```bash
python3 src/kg/query_kg.py
```

**6. Prepare KGE splits**
```bash
python3 src/kge/prepare_kge.py
# → data/kge/train.txt  valid.txt  test.txt
```

**7. Train TransE (no GPU needed)**
```bash
python3 src/kge/simple_kge.py
```

**8. Train with PyKEEN (optional, GPU recommended)**
```bash
python3 src/kge/train_kge.py
```

---

## How to run the RAG demo
```bash
python3 src/rag/rag_demo.py
```

Supported question patterns:
- `Who directed <film>?`
- `Which actors played in <film>?`
- `Who acted in <film>?`
```
=== Simple RAG Demo ===
Your question: Who directed Babygirl?

Generated SPARQL query:
PREFIX ex: <http://example.org/>
SELECT ?director WHERE { ex:Babygirl ex:directedBy ?director . }

Answer: Halina Reijn
```

If the exact entity is not found, the system falls back to fuzzy matching.
If the entity is not in the graph at all, it returns: `This entity is not in the knowledge graph.`

---

## Hardware requirements

| Task | Requirement |
|------|-------------|
| Crawling | Internet access |
| KGE — simple_kge.py | CPU, 2 GB RAM |
| KGE — train_kge.py (PyKEEN) | GPU recommended |
| RAG demo | CPU, 1 GB RAM |

---

## Knowledge Graph statistics

| Metric | Value |
|--------|-------|
| Films | 83 |
| Directors | 75 |
| Actors | 259 |
| Total triples | 379 |
| Relations | 2 — directedBy, actedIn |
| owl:sameAs links (DBpedia) | 417 |
| Formats | Turtle (.ttl), N-Triples (.nt) |

TransE results (simple_kge.py): MRR 0.056 · Hits@1 0.013 · Hits@10 0.171

---

## Notes

- `data/samples/` contains pre-generated files — the RAG demo runs without re-crawling.
- `kg_artifacts/alignment.ttl` maps every local entity to its DBpedia URI via `owl:sameAs`.
- `kg_artifacts/ontology.ttl` defines classes Film, Director, Actor with domain/range constraints.