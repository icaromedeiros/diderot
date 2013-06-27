import os
from sets import Set

from urllib import urlopen
from urlparse import urlparse

from rdflib import Graph, StringInputSource

from diderot.OWL import OWLNS

SUPPORTED_URL_SCHEMES = ("http", "https", "file")
AVAILABLE_INPUT_FORMATS_MESSAGE = "Available formats: a string URI, a string relative file path," + \
    " a string in N3/Turtle format, or a rdflib.Graph object."
EMPTY_GRAPH_MESSAGE = "The graph has no triples"


def parse_facts(facts, begin=None, end=None):
    """
        Utility function to parse facts in multiple formats``.

        Available formats for input: a string URI, a string relative file path,
        a string in ``N3/Turtle`` format, or a ``rdflib.Graph`` object.

        A ``RuntimeError`` will be raised if the input is:

        * An URI in a scheme different than ``http``, ``https``, or ``file``.

        * An invalid string representing a graph in ``N3/Turtle`` format.

        * An object different than string or ``RDFlib.Graph``.

        The optional parameters ``begin`` and ``end`` are used to extract
        a fragment of the original file, if the input is a relative file path.
    """
    if isinstance(facts, str):
        scheme = urlparse(facts).scheme
        try:
            if scheme:
                if scheme not in SUPPORTED_URL_SCHEMES:
                    raise RuntimeError("URI scheme not recognized. Supported: {0}".format(SUPPORTED_URL_SCHEMES))
                else:  # Assume it is an URI
                    url_content = urlopen(facts)
                    facts_string = "".join(url_content.readlines())
                    facts_graph = parse_ttl_string(facts_string)
            else:  # Assume it is a file path
                file_path = os.getcwd() + "/" + facts
                facts_graph = parse_ttl_file(file_path, begin, end)

        except IOError:  # Assume it is a string in N3/Turle format
            try:
                facts_graph = parse_ttl_string(facts)
            except Exception as e:
                facts_excerpt = facts[:30]
                if len(facts) > 30:
                    facts_excerpt += " ..."
                PARSING_ERROR_MSG = "Error parsing facts.\n  {0}\n  Input: {1}\n  Exception: {2}".format(
                    AVAILABLE_INPUT_FORMATS_MESSAGE, facts_excerpt, e.message)
                raise RuntimeError(PARSING_ERROR_MSG)
        if is_empty_graph(facts_graph):
            raise RuntimeError(EMPTY_GRAPH_MESSAGE)
        return facts_graph
    elif isinstance(facts, Graph):
        if is_empty_graph(facts):
            raise RuntimeError(EMPTY_GRAPH_MESSAGE)
        return facts
    else:
        input_type = str(type(facts))
        PARSING_ERROR_MSG = "Unaccepted input.\n  {0}\n  Input type: {1}".\
            format(AVAILABLE_INPUT_FORMATS_MESSAGE, input_type)
        RuntimeError(PARSING_ERROR_MSG)


def parse_ttl_string(ttl_string):
    """
        Utility function that, given a string in ``N3/Turtle`` format
        will parse it and return the equivalent ``rdflib.Graph`` object.
    """
    graph = get_empty_graph()
    graph.parse(StringInputSource(ttl_string), format="n3")
    return graph


def parse_ttl_file(ttl_file_path, begin=None, end=None):
    """
        Utility function that given a file path return the ``rdflib.Graph``
        correspondent to the file content.

        The optional parameters ``begin`` and ``end`` are used to extract
        a fragment of the original file.

        If parameters ``begin`` or ``end`` are not positive integers a
        ``RuntimeError`` will be raised.
    """
    INVALID_PARAMETER_MESSAGE = "Parameter begin and end should be positive integers or None"
    try:
        if (begin is not None and int(begin) <= 0):
            raise RuntimeError(INVALID_PARAMETER_MESSAGE)

        if (end is not None and int(end) <= 0):
            raise RuntimeError(INVALID_PARAMETER_MESSAGE)
    except ValueError:
        raise RuntimeError(INVALID_PARAMETER_MESSAGE)

    # So the first line is 0
    if begin is not None:
        begin = begin - 1
    if end is not None:
        end = end - 1
    ttl_file = open(ttl_file_path)
    lines = ttl_file.readlines()

    if begin is not None and end is not None:
        ttl_string = "".join(lines[begin:end])
    elif begin is not None:
        ttl_string = "".join(lines[begin:])
    elif end is not None:
        ttl_string = "".join(lines[:end])
    else:
        ttl_string = "".join(lines)

    return parse_ttl_string(ttl_string)


def get_empty_graph():
    """
        Utility function to create an empty ``RDFlib.Graph``
        with the ``OWL`` namespace enabled.
    """
    graph = Graph()
    graph.bind("owl", OWLNS, override=True)
    return graph


def is_triples_subset(graph1, graph2):
    """
        Utility function that compares ``graph1`` and ``graph2``
        to check if ``graph1`` is a subset of ``graph2``.

        If any parameter is ``None`` or if ``graph1`` is empty a
        ``RuntimeError`` is raised.
    """
    if graph1 is None or graph2 is None:
        raise RuntimeError("Given graphs should not be None")
    if is_empty_graph(graph1):
        raise RuntimeError("First graph must not be empty")
    return Set(graph1).issubset(Set(graph2))


def is_empty_graph(graph):
    """
        Utility function to check if a given ``RDFlib.Graph``
        is empty.
    """
    return len(graph) == 0
