from unittest import TestCase
from mock import patch, mock_open
from StringIO import StringIO

from rdflib import RDF, URIRef

from diderot import OWL
from diderot.utils import parse_ttl_string, parse_ttl_file, get_empty_graph,\
    parse_facts, is_triples_subset, is_empty_graph
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
        self.assertRaises(RuntimeError, parse_ttl_file, None, begin=0)

    def test_parse_ttl_file_with_invalid_begin_end_0(self):
        self.assertRaises(RuntimeError, parse_ttl_file, None, end=0)

    def test_is_triple_subset(self):
        larger_graph = get_empty_graph()
        larger_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        larger_graph.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        larger_graph.add((URIRef(":Human"), RDF.type, OWL.Class))

        subset_graph = get_empty_graph()
        subset_graph.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        self.assertTrue(is_triples_subset(subset_graph, larger_graph))

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

    @patch("diderot.utils.parse_ttl_string", return_value=NON_EMPTY_GRAPH)
    def test_parse_facts_from_file_path(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch("diderot.utils.urlopen", mocked_open):
            parse_facts("db/test.n3")
            parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("diderot.utils.parse_ttl_string", return_value=NON_EMPTY_GRAPH)
    def test_parse_facts_from_string(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.side_effect = IOError
        with patch("diderot.utils.urlopen", mocked_open):
            parse_facts(TTL_STRING)
            parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("diderot.utils.parse_ttl_string", side_effect=RuntimeError)
    def test_parse_facts_from_invalid_string(self, parse_ttl_string):
        INVALID_FACTS_STRING = "<rdf>INVALID</rdf>"
        mocked_open = mock_open()
        mocked_open.side_effect = IOError
        with patch("diderot.utils.urlopen", mocked_open):
            self.assertRaises(RuntimeError, parse_facts, INVALID_FACTS_STRING)

    def test_parse_facts_rdflib_graph(self):
        graph = get_empty_graph()
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
