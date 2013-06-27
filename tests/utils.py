from rdflib import Namespace

EXAMPLE = Namespace("http://example.onto/")


def graph_to_list_of_triples(graph):
    list_of_triples = []
    for triple in graph:
        list_of_triples.append(triple)
    return list_of_triples


def add_example_namespace(graph):
    graph.bind("ex", EXAMPLE)
    return graph
