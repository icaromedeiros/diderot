from unittest import TestCase
from rdflib import RDF, RDFS, URIRef

from marvin import can_infer, OWL
from marvin.utils import get_empty_graph


class InferringExpectedFactsTestCase(TestCase):

    def test_subclass_assertion(self):
        facts = get_empty_graph()
        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mortal")))
        facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Human")))

        expected_facts = get_empty_graph()
        expected_facts.add((URIRef(":Icaro"), RDF.type, URIRef(":Mortal")))
        expected_facts.add((URIRef(":Mortal"), RDF.type, OWL.Class))
        expected_facts.add((URIRef(":Human"), RDF.type, OWL.Class))

        assertion = can_infer(expected_facts).from_facts(facts)
        self.assertTrue(assertion.assertion_value)

#    def test_subclass_transitivity(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Mammal")))
#        facts.add((URIRef(":Mammal"), RDFS.subClassOf, URIRef(":Animal")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Human"), RDFS.subClassOf, URIRef(":Animal")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
#
#    def test_inverseof_property_inferences(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":has_parent"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":is_parent_of"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":has_parent"), OWL.inverseOf, URIRef(":is_parent_of")))
#        facts.add((URIRef(":Icaro"), URIRef(":has_parent"), URIRef(":Roberto")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Roberto"), URIRef(":is_parent_of"), URIRef(":Icaro")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
#
#    def test_symmetric_property_inferences(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":has_sibling"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":has_sibling"), RDF.type, OWL.SymmetricProperty))
#        facts.add((URIRef(":Icaro"), URIRef(":has_sibling"), URIRef(":Ana")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Ana"), URIRef(":has_sibling"), URIRef(":Icaro")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
#
#    def test_transitive_property_inferences(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":has_ancestror"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":has_ancestror"), RDF.type, OWL.TransitiveProperty))
#        facts.add((URIRef(":Icaro"), URIRef(":has_ancestror"), URIRef(":Roberto")))
#        facts.add((URIRef(":Roberto"), URIRef(":has_ancestror"), URIRef(":Antonio")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Icaro"), URIRef(":has_ancestror"), URIRef(":Antonio")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
#
#    def test_functional_property_inferences(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":has_father"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":has_father"), RDF.type, OWL.FunctionalProperty))
#        facts.add((URIRef(":Icaro"), URIRef(":has_father"), URIRef(":Roberto")))
#        facts.add((URIRef(":Icaro"), URIRef(":has_father"), URIRef(":Jose_Roberto")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Roberto"), OWL.sameAs, URIRef(":Jose_Roberto")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
#
#    def test_inverse_functional_property_inferences(self):
#        facts = get_empty_graph()
#        facts.add((URIRef(":biological_father"), RDF.type, OWL.ObjectProperty))
#        facts.add((URIRef(":biological_father"), RDF.type, OWL.InverseFunctionalProperty))
#        facts.add((URIRef(":Roberto"), URIRef(":biological_father"), URIRef(":Icaro")))
#        facts.add((URIRef(":Jose_Roberto"), URIRef(":biological_father"), URIRef(":Icaro")))
#
#        expected_facts = get_empty_graph()
#        expected_facts.add((URIRef(":Roberto"), OWL.sameAs, URIRef(":Jose_Roberto")))
#
#        assertion = can_infer(expected_facts).from_facts(facts)
#        self.assertTrue(assertion.assertion_value)
