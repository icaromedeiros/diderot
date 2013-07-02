from diderot import DiderotTestCase, cannot_infer


class ExpectedFactsTestCase(DiderotTestCase):

    def test_check_unexpected_facts(self):
        UNEXPECTED_FACTS = "<http://example.onto/Icaro> a <http://example.onto/Student> ."
        ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
        self.assert_that(cannot_infer(UNEXPECTED_FACTS).from_facts(ONTOLOGY_FILE))

    # Just to see error messages

    #def test_check_unexpected_facts_can_be_inferred(self):
    #    UNEXPECTED_FACTS = "<http://example.onto/Icaro> a <http://example.onto/Mortal> ."
    #    ONTOLOGY_FILE = "example/db/check_expected_facts/ontology.n3"
    #    self.assert_that(cannot_infer(UNEXPECTED_FACTS).from_facts(ONTOLOGY_FILE))

EXPECTED_ANSWER = [(anyURI(), anyInt(), anyString())]
self.assert_that(can_answer(QUESTION).from_ontology(ONTOLOGY_FILE).with_answer(EXPECTED_ANSWER))

import sure

(5).should.be.an('int')
