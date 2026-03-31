from owlready2 import get_ontology, sync_reasoner_pellet
from rdflib import Graph

EX = "http://example.org/"
onto = get_ontology(EX)

with onto:
    from owlready2 import Thing, ObjectProperty

    class Film(Thing):
        pass

    class Person(Thing):
        pass

    class Director(Person):
        pass

    class Actor(Person):
        pass

    class directedBy(ObjectProperty):
        domain = [Film]
        range  = [Director]

    class directed(ObjectProperty):
        inverse_property = directedBy
        domain = [Director]
        range  = [Film]

    class actedIn(ObjectProperty):
        domain = [Actor]
        range  = [Film]

    class hasActor(ObjectProperty):
        inverse_property = actedIn
        domain = [Film]
        range  = [Actor]

    class workedWith(ObjectProperty):
        domain    = [Person]
        range     = [Person]
        symmetric = True


def load_individuals(kg_path="../kg/kg.ttl"):
    g = Graph()
    g.parse(kg_path, format="turtle")
    added = 0
    with onto:
        for s, p, o in g:
            s_local = str(s).replace(EX, "")
            o_local = str(o).replace(EX, "")
            pred    = str(p).replace(EX, "")
            if pred == "directedBy":
                Film(s_local).directedBy.append(Director(o_local))
                added += 1
            elif pred == "actedIn":
                Film(s_local).hasActor.append(Actor(o_local))
                added += 1
    return added


def apply_rules():
    from owlready2 import Imp
    with onto:
        r1 = Imp()
        r1.set_as_rule(
            "ex:Film(?f), ex:directedBy(?f, ?d), ex:hasActor(?f, ?a)"
            " -> ex:workedWith(?d, ?a)",
            namespaces={"ex": EX}
        )
        r2 = Imp()
        r2.set_as_rule(
            "ex:workedWith(?a, ?b) -> ex:workedWith(?b, ?a)",
            namespaces={"ex": EX}
        )


def main():
    n = load_individuals()
    print(f"Loaded {n} triples as OWL individuals")
    apply_rules()
    try:
        with onto:
            sync_reasoner_pellet(infer_property_values=True)
        print("Reasoner finished")
    except Exception as e:
        print(f"Reasoner note: {e}")

    pairs = []
    for ind in onto.individuals():
        if hasattr(ind, "workedWith"):
            for colleague in ind.workedWith:
                pairs.append((ind.name, colleague.name))

    print(f"\nInferred workedWith pairs: {len(pairs)}")
    for a, b in pairs[:10]:
        print(f"  {a.replace('_', ' ')}  --workedWith-->  {b.replace('_', ' ')}")


if __name__ == "__main__":
    main()
