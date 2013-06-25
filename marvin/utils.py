import os
import sys
import traceback

from urllib import urlopen
from urlparse import urlparse, urljoin

from rdflib import Graph, StringInputSource

from marvin.OWL import OWLNS

SUPPORTED_URL_SCHEMES = ("http", "https", "file")
AVAILABLE_INPUT_FORMATS_MESSAGE = "Available formats: a string URI, a string relative file path," + \
    "a string in N3/Turle format, or a rdflib.Graph object."


def parse_facts(facts):
    if isinstance(facts, str):
        url_string = facts
        scheme = urlparse(url_string).scheme

        if scheme:
            if scheme not in SUPPORTED_URL_SCHEMES:
                raise RuntimeError("URI scheme not recognized. Supported: {0}".format(SUPPORTED_URL_SCHEMES))
            else:  # Assume it is a file path
                url_string = urljoin(os.getcwd(), url_string)

        try:
            url_content = urlopen(url_string)
            facts = "".join(url_content.readlines())
            facts_graph = parse_ttl_string(facts)
        except IOError:  # Assume it is a string in N3/Turle format
            try:
                facts_graph = parse_ttl_string(facts)
            except Exception as e:
                etype, value, tb = sys.exc_info()
                error_msg = ''.join(traceback.format_exception(etype, value, tb))
                facts_excerpt = facts[:30]
                PARSING_ERROR_MSG = "Error parsing facts.\n  {0}\n" +\
                        "  Input: {1}\n  Exception: {2}".format(AVAILABLE_INPUT_FORMATS_MESSAGE,
                                                                facts_excerpt, error_msg)
                raise RuntimeError(PARSING_ERROR_MSG)
        return facts_graph
    elif isinstance(facts, Graph):
        return facts
    else:
        input_type = str(type(facts))
        PARSING_ERROR_MSG = "Unaccepted input.\n  {0}\n  Input type: {1}".\
            format(AVAILABLE_INPUT_FORMATS_MESSAGE, input_type)
        RuntimeError(PARSING_ERROR_MSG)


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
