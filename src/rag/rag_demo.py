from rdflib import Graph
from difflib import get_close_matches
import re

g = Graph()
g.parse("data/samples/kg.ttl", format="turtle")

PREFIX = "PREFIX ex: <http://example.org/>\n"

def normalize_entity(text):
    # Clean punctuation first, then normalise
    text = re.sub(r"[?.!]+$", "", text.strip())
    text = text.strip().title().replace(" ", "_")

    aliases = {
        "Titanic":    "Titanic_(1997_film)",
        "Gladiator":  "Gladiator_(2000_film)",
        "The_Matrix": "The_Matrix",
        "Inception":  "Inception",
    }
    return aliases.get(text, text)

def find_closest_entity(name):
    entities = set()
    for s, p, o in g:
        entities.add(str(s).split("/")[-1])
        entities.add(str(o).split("/")[-1])
    matches = get_close_matches(name, entities, n=1, cutoff=0.6)
    if matches:
        return matches[0]
    return name

def run_query(sparql):
    try:
        results = g.query(sparql)
        return [str(row[0]).split("/")[-1].replace("_", " ") for row in results]
    except Exception:
        return []

def question_to_sparql(question):
    q = question.strip().lower()
    q = re.sub(r"[?.!]+$", "", q).strip()

    m = re.match(r"who directed (.+)", q)
    if m:
        film = normalize_entity(m.group(1))
        film = find_closest_entity(film)
        query = PREFIX + f"SELECT ?director WHERE {{ ex:{film} ex:directedBy ?director . }}"
        return query, "director"

    m = re.match(r"(which actors played in|who acted in|who starred in) (.+)", q)
    if m:
        film = normalize_entity(m.group(2))
        film = find_closest_entity(film)
        query = PREFIX + f"SELECT ?actor WHERE {{ ex:{film} ex:actedIn ?actor . }}"
        return query, "actor"

    return None, None

def self_repair(question):
    return re.sub(r"[?.!]+$", "", question.strip()).strip()

def main():
    print("=== Simple RAG Demo ===")
    print("Examples:")
    print("- Who directed Babygirl?")
    print("- Which actors played in A Big Case?")
    print("- Type 'exit' to quit")

    while True:
        question = input("\nYour question: ").strip()

        if question.lower() == "exit":
            break

        query, answer_type = question_to_sparql(question)

        if query is None:
            repaired = self_repair(question)
            query, answer_type = question_to_sparql(repaired)

        if query is None:
            print("I could not understand the question format.")
            continue

        print("\nGenerated SPARQL query:")
        print(query)

        answers = run_query(query)

        if answers:
            print("\nAnswer:")
            print(", ".join(answers))
        else:
            print("\nThis entity is not in the knowledge graph.")

if __name__ == "__main__":
    main()