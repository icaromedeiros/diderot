from diderot import DiderotTestCase, can_answer
from rdflib import URIRef

class ExpectedFactsTestCase(DiderotTestCase):

    def test_check_can_answer(self):
        QUESTION = """
        SELECT ?human ?age ?name
        WHERE {
            ?human a                          <http://example.onto/Human> ;
                   <http://example.onto/age>  26 ;
                   <http://example.onto/name> "Icaro" .
        }
        """
        ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
        self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))

    def test_check_can_answer_with_ask(self):
        QUESTION = """
        ASK {
            ?human a <http://example.onto/Human> ;
        }
        """
        ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
        self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))


    def test_check_can_answer_with_answer(self):
        QUESTION = """
        SELECT ?human ?age ?name
        WHERE {
            ?human a                          <http://example.onto/Human> ;
                   <http://example.onto/age>  ?age ;
                   <http://example.onto/name> ?name .
        }
        """
        EXPECTED_ANSWER = [(URIRef("http://example.onto/Icaro"), 26, "Icaro")]
        ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
        self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE).\
                         with_answer(EXPECTED_ANSWER))

    # Just to see error messages

    #def test_check_can_answer_with_ask_returns_false(self):
    #    QUESTION = """
    #    ASK {
    #        ?god a <http://example.onto/God> .
    #    }
    #    """
    #    ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
    #    self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))

    #def test_check_can_answer_with_answer_with_ask_query_raise_exception(self):
    #    QUESTION = """
    #    ASK {
    #        ?human a <http://example.onto/Human> .
    #    }
    #    """
    #    ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
    #    EXPECTED_ANSWER = [(URIRef("http://example.onto/Icaro"),)]
    #    self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE).with_answer(EXPECTED_ANSWER))

    #def test_check_can_answer_with_answer_dont_match_expected_answer(self):
    #    QUESTION = """
    #    SELECT ?human ?age ?name
    #    WHERE {
    #        ?human a                          <http://example.onto/Human> ;
    #               <http://example.onto/age>  ?age ;
    #               <http://example.onto/name> ?name .
    #    }
    #    """
    #    EXPECTED_ANSWER = [(URIRef("http://example.onto/Icaro"), 64, "Icaro Medeiros")]
    #    ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
    #    self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE).\
    #                     with_answer(EXPECTED_ANSWER))
