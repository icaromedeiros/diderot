from diderot import DiderotTestCase, can_answer


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

    # Just to see error messages

    #def test_check_can_answer_with_ask_returns_false(self):
    #    QUESTION = """
    #    ASK {
    #        ?god a <http://example.onto/God> ;
    #    }
    #    """
    #    ONTOLOGY_FILE = "example/db/answering_competency_question/ontology.n3"
    #    self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE))
