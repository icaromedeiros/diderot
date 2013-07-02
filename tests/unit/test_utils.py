import os

from unittest import TestCase
from mock import patch, mock_open
from StringIO import StringIO

from rdflib import RDF, URIRef

from diderot import OWL
from diderot.utils import parse_ttl_string, parse_ttl_file, get_empty_graph,\
    parse_facts, is_empty_graph, difference, intersection
from tests.utils import graph_to_list_of_triples, add_example_namespace, EXAMPLE


TTL_STRING = """@prefix : <http://example.onto/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:Icaro a :Mortal .
:Mortal a owl:Class .
:Human a owl:Class ."""


NON_EMPTY_GRAPH = get_empty_graph()
NON_EMPTY_GRAPH.add((EXAMPLE.Icaro, RDF.type, EXAMPLE.Mortal))


class UtilsTestCase(TestCase):

    def test_from_ttl_to_string(self):
        expected_graph = get_empty_graph()
        expected_graph = add_example_namespace(expected_graph)

        expected_graph.add((EXAMPLE.Icaro, RDF.type, EXAMPLE.Mortal))
        expected_graph.add((EXAMPLE.Mortal, RDF.type, OWL.Class))
        expected_graph.add((EXAMPLE.Human, RDF.type, OWL.Class))
        expected_triples_list = graph_to_list_of_triples(expected_graph)

        result = parse_ttl_string(TTL_STRING)
        result = graph_to_list_of_triples(result)
        self.assertItemsEqual(result, expected_triples_list)

    @patch("diderot.utils.parse_ttl_string")
    def test_parse_ttl_file(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open)
        parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("diderot.utils.parse_ttl_string")
    def test_parse_ttl_file_with_begin(self, parse_ttl_string):
        EXPECTED_STRING = ":Human a owl:Class ."
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open, begin=6)
        parse_ttl_string.assert_called_with(EXPECTED_STRING)

    @patch("diderot.utils.parse_ttl_string")
    def test_parse_ttl_file_with_end(self, parse_ttl_string):
        EXPECTED_STRING = "@prefix : <http://example.onto/> .\n"

        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open, end=2)
        parse_ttl_string.assert_called_with(EXPECTED_STRING)

    @patch("diderot.utils.parse_ttl_string")
    def test_parse_ttl_file_with_begin_and_end(self, parse_ttl_string):
        EXPECTED_STRING = "@prefix : <http://example.onto/> .\n"

        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open, begin=1, end=2)
        parse_ttl_string.assert_called_with(EXPECTED_STRING)

    def test_parse_ttl_file_with_invalid_begin(self):
        self.assertRaises(RuntimeError, parse_ttl_file, "file_path", begin=0)

    def test_parse_ttl_file_with_invalid_begin_as_string(self):
        self.assertRaises(RuntimeError, parse_ttl_file, "file_path", begin="invalid")

    def test_parse_ttl_file_with_invalid_end_0(self):
        self.assertRaises(RuntimeError, parse_ttl_file, "file_path", end=0)

    def test_difference(self):
        larger_graph = get_empty_graph()
        larger_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        larger_graph.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        larger_graph.add((URIRef(":Human"), RDF.type, OWL.Class))

        subset_graph = get_empty_graph()
        subset_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        self.assertTrue(is_empty_graph(difference(subset_graph, larger_graph)))

    def test_difference_not_empty(self):
        larger_graph = get_empty_graph()
        larger_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        larger_graph.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        larger_graph.add((URIRef(":Human"), RDF.type, OWL.Class))

        subset_graph = get_empty_graph()
        subset_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        subset_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Student")))  # Not in larger_graph

        difference_expected_graph = get_empty_graph()
        difference_expected_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Student")))  # Not in larger_graph

        difference_expected_graph_set = set(difference_expected_graph)

        difference_result_graph_set = difference(subset_graph, larger_graph)

        self.assertEqual(len(difference_result_graph_set), 1)
        self.assertEqual(difference_expected_graph_set, difference_result_graph_set)

    def test_difference_empty_subgraph(self):
        larger_graph = get_empty_graph()
        subset_graph = get_empty_graph()
        self.assertRaises(RuntimeError, difference, subset_graph, larger_graph)

    def test_difference_larger_graph_None(self):
        subset_graph = get_empty_graph()
        self.assertRaises(RuntimeError, difference, subset_graph, None)

    def test_difference_subset_graph_None(self):
        larger_graph = get_empty_graph()
        self.assertRaises(RuntimeError, difference, None, larger_graph)

    def test_intersection(self):
        larger_graph = get_empty_graph()
        larger_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        larger_graph.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        larger_graph.add((URIRef(":Human"), RDF.type, OWL.Class))

        subset_graph = get_empty_graph()
        subset_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))

        result = intersection(subset_graph, larger_graph)
        expected = set(subset_graph)
        self.assertEqual(result, expected)

    def test_intersection_empty_graphs(self):
        larger_graph = get_empty_graph()
        subset_graph = get_empty_graph()
        self.assertRaises(RuntimeError, intersection, subset_graph, larger_graph)

    def test_intersection_larger_graph_None(self):
        subset_graph = get_empty_graph()
        self.assertRaises(RuntimeError, intersection, subset_graph, None)

    def test_intersection_subset_graph_None(self):
        larger_graph = get_empty_graph()
        self.assertRaises(RuntimeError, difference, None, larger_graph)

    @patch("diderot.utils.parse_ttl_string", return_value=NON_EMPTY_GRAPH)
    def test_parse_facts_from_uri(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch("diderot.utils.urlopen", mocked_open):
            parse_facts("http://test")
            parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("diderot.utils.parse_ttl_string")
    def test_parse_facts_from_uri_in_unavaiable_protocol(self, parse_ttl_string):
        self.assertRaises(RuntimeError, parse_facts, "ftp://test.com")

    @patch("diderot.utils.parse_ttl_file", return_value=NON_EMPTY_GRAPH)
    def test_parse_facts_from_file_path(self, parse_ttl_file):
        parse_facts("db/test.n3", begin=2, end=3)
        parse_ttl_file.assert_called_with(os.getcwd() + "/db/test.n3", 2, 3)

    @patch("diderot.utils.parse_ttl_string", return_value=NON_EMPTY_GRAPH)
    def test_parse_facts_from_string(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.side_effect = IOError
        with patch("diderot.utils.urlopen", mocked_open):
            parse_facts(TTL_STRING)
            parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("diderot.utils.parse_ttl_string", side_effect=RuntimeError)
    def test_parse_facts_from_invalid_string(self, parse_ttl_string):
        INVALID_FACTS_STRING = "<rdf>THIS IS AN INVALID STRING. ONLY N3 IS ACCEPTED</rdf>"
        mocked_open = mock_open()
        mocked_open.side_effect = IOError
        with patch("diderot.utils.urlopen", mocked_open):
            self.assertRaises(RuntimeError, parse_facts, INVALID_FACTS_STRING)

    def test_parse_facts_with_empty_graph_string(self):
        EMPTY_GRAPH_TTL_STRING = """
        @prefix : <http://example.onto/> .
        @prefix owl: <http://www.w3.org/2002/07/owl#> .
        """
        self.assertRaises(RuntimeError, parse_facts, EMPTY_GRAPH_TTL_STRING)

    def test_parse_facts_with_empty_rdflib_graph(self):
        graph = get_empty_graph()
        self.assertRaises(RuntimeError, parse_facts, graph)

    def test_parse_facts_rdflib_graph(self):
        graph = get_empty_graph()
        graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        self.assertEqual(graph, parse_facts(graph))

    def test_parse_facts_invalid_type(self):
        self.assertRaises(RuntimeError, parse_facts(10))

    def test_is_empty_graph(self):
        graph = get_empty_graph()
        self.assertTrue(is_empty_graph(graph))

    def test_is_not_empty_graph(self):
        graph = get_empty_graph()
        graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        self.assertFalse(is_empty_graph(graph))
