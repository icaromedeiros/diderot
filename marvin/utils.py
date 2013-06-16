from urllib import urlopen

from rdflib import Graph, StringInputSource

from marvin.OWL import OWLNS


def parse_facts(facts):
    if isinstance(facts, str):
        try:
            url_content = urlopen(facts)
            facts = "".join(url_content.readlines())
            facts_graph = parse_ttl_string(facts)
        except IOError:
            try:
                facts_graph = parse_ttl_string(facts)
            except:
                facts_excerpt = facts[:30]
                raise RuntimeError("Error parsing facts:\n  " + facts_excerpt)
        return facts_graph
    elif isinstance(facts, Graph):
        return facts
    else:
        RuntimeError("Not accepted facts input: Available: a string URI, " +
                     "string with a Turle content or rdflib.Graph")


def parse_ttl_string(ttl_string):
    graph = get_empty_graph()
    graph.parse(StringInputSource(ttl_string), format="n3")
    return graph


def parse_ttl_file(ttl_file, begin=None, end=None):
    if (begin is not None and begin <= 0) or (end is not None and end <= 0):
        raise RuntimeError("")
    # So the first line is 0
    if begin is not None:
        begin = begin - 1
    if end is not None:
        end = end - 1
    ttl_file = open(ttl_file)
    lines = ttl_file.readlines()

    if begin is not None and end is not None:
        ttl_string = "".join(lines[begin:end])
    elif begin is not None:
        ttl_string = "".join(lines[begin:])
    elif end is not None:
        ttl_string = "".join(lines[:end])
    else:
        ttl_string = "".join(lines)

    parse_ttl_string(ttl_string)


def get_empty_graph():
    graph = Graph()
    graph.bind("owl", OWLNS, override=True)
    return graph


def is_triples_subset(graph1, graph2):
    for triple in graph1.triples((None, None, None)):
        if triple in graph2:
            is_subset = True
        else:
            is_subset = False
            break
    return is_subset
