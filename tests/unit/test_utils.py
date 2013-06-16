from unittest import TestCase
from mock import patch, mock_open
from StringIO import StringIO

from rdflib import RDF, URIRef

from marvin import OWL
from marvin.utils import parse_ttl_string, parse_ttl_file, get_empty_graph,\
    parse_facts, is_triples_subset
from tests.utils import graph_to_list_of_triples, add_example_namespace, EXAMPLE


TTL_STRING = """@prefix : <http://example.onto/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .

:Icaro a :Mortal .
:Mortal a owl:Class .
:Human a owl:Class ."""


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

    @patch("marvin.utils.parse_ttl_string")
    def test_parse_ttl_file(self, parse_ttl_string):
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open)
        parse_ttl_string.assert_called_with(TTL_STRING)

    @patch("marvin.utils.parse_ttl_string")
    def test_parse_ttl_file_with_begin(self, parse_ttl_string):
        EXPECTED_STRING = ":Human a owl:Class ."
        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open, begin=6)
        parse_ttl_string.assert_called_with(EXPECTED_STRING)

    @patch("marvin.utils.parse_ttl_string")
    def test_parse_ttl_file_with_end(self, parse_ttl_string):
        EXPECTED_STRING = "@prefix : <http://example.onto/> .\n"

        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch('__builtin__.open', mocked_open):
            parse_ttl_file(mocked_open, end=2)
        parse_ttl_string.assert_called_with(EXPECTED_STRING)

    @patch("marvin.utils.parse_ttl_string")
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

    def test_parse_facts_from_uri(self):
        expected_graph = get_empty_graph()
        expected_graph = add_example_namespace(expected_graph)
        expected_graph.add((EXAMPLE.Icaro, RDF.type, EXAMPLE.Mortal))
        expected_graph.add((EXAMPLE.Mortal, RDF.type, OWL.Class))
        expected_graph.add((EXAMPLE.Human, RDF.type, OWL.Class))

        mocked_open = mock_open()
        mocked_open.return_value = StringIO(TTL_STRING)
        with patch("marvin.utils.urlopen", mocked_open):
            result = parse_facts("file://test")
            self.assertTrue(is_triples_subset(result, expected_graph))

    def test_parse_facts_from_string(self):
        expected_graph = get_empty_graph()
        expected_graph = add_example_namespace(expected_graph)
        expected_graph.add((EXAMPLE.Icaro, RDF.type, EXAMPLE.Mortal))
        expected_graph.add((EXAMPLE.Mortal, RDF.type, OWL.Class))
        expected_graph.add((EXAMPLE.Human, RDF.type, OWL.Class))

        mocked_open = mock_open()
        mocked_open.side_effect = IOError
        with patch("marvin.utils.urlopen", mocked_open):
            result = parse_facts(TTL_STRING)
            self.assertTrue(is_triples_subset(result, expected_graph))
