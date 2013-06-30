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
        self.assertThat(can_answer("SELECT * WHERE {?s ?p ?o}").from_ontology(ONTOLOGY_FILE))


